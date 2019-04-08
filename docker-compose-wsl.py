# Python Standard Libraries
import os
import sys
import subprocess
import pathlib
import re

# Variable(s)
compose_file_tmp_dir = os.path.join(os.path.expandvars('%userprofile%'), 'AppData', 'Local', 'Temp')
cli_args = sys.argv[1:]
docker_compose_cli_args = ''
bash_variables = ''

# Function(s)
def wsl_drive_map(string_to_map):
    '''
    Replace all the instance of the drive(s) letter(s) to their corresponding WSL mount point

    :param path:
    :return:
    '''
    mapped_string = string_to_map

    paths_regex = re.compile(r'([A-Za-z]+:[\\|/|\\\\][^:]+)')
    for windows_path_match in re.finditer(paths_regex, string_to_map):
        windows_path = windows_path_match.group(1)

        if os.path.exists(windows_path):
            drives_regex = re.compile(r'([A-Za-z]+):[\\|/|\\\\]')

            for drive in re.finditer(drives_regex, windows_path):
                windows_drive = drive.group(1)
                wsl_mount = '/{0}/'.format(windows_drive.lower())

                mapped_string = re.sub(r'{0}:[\\|/|\\\\]'.format(windows_drive), wsl_mount, mapped_string)
                mapped_string = mapped_string.replace('\\', '/').replace('\\\\', '/')

    return mapped_string

# Add the docker variable(s), defined in the Windows environment variable(s) to the docker-compose command
for key, value in os.environ.items():
    if key.startswith('DOCKER'):

        try:
            value = int(value)
        except ValueError:
            pass

        if isinstance(value, int):
            bash_variables += '{0}={1} '.format(key, value)
        else:
            bash_variables += '{0}="{1}" '.format(key, value)

# Replace Windows path with WSL supported path
for idx, cli_arg in enumerate(cli_args):

    if idx != 0 and cli_args[idx - 1] == '-f':
        compose_file = cli_arg
        compose_file_name = os.path.basename(compose_file)
        tmp_compose_file = os.path.join(compose_file_tmp_dir, compose_file_name)

        if os.path.isfile(compose_file):
            compose_file_content = pathlib.Path(compose_file).read_text()
            new_compose_file_content = wsl_drive_map(compose_file_content)
            pathlib.Path(tmp_compose_file).write_text(new_compose_file_content)
        else:
            sys.stderr.write('The PyCharm docker-compose file "{0}" does not exists, exiting...'.format(
                compose_file))
            raise SystemExit(1)

        compose_file_mapped = wsl_drive_map(tmp_compose_file)
        docker_compose_cli_args += '{0} '.format(compose_file_mapped)

    else:
        docker_compose_cli_args += '{0} '.format(cli_arg)

docker_compose_cmd = ['C:\\Windows\\System32\\bash.exe', '-c', '{0} docker-compose {1}'.format(
        bash_variables,
        docker_compose_cli_args
    )
]

print('The docker-compose bash variable(s) were: {0}'.format(bash_variables))
print('The docker-compose argument(s) were: {0}'.format(docker_compose_cli_args))
print('The docker-compose command was: {0}'.format(' '.join(docker_compose_cmd)))

# Run the docker-compose binary in bash on WSL with the appropriate argument(s)
subprocess.run(docker_compose_cmd, shell=True)

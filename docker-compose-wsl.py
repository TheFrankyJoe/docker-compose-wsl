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
    windows_file_path = cli_arg

    if idx != 0 and cli_args[idx - 1] == '-f':
        compose_file = cli_arg
        compose_file_name = os.path.basename(compose_file)
        windows_file_path = os.path.join(compose_file_tmp_dir, compose_file_name)

        if os.path.isfile(compose_file):
            compose_file_content = pathlib.Path(compose_file).read_text()
            new_compose_file_content = wsl_drive_map(compose_file_content)
            pathlib.Path(windows_file_path).write_text(new_compose_file_content)
        else:
            sys.stderr.write('The PyCharm docker-compose file "{0}" does not exists, exiting...'.format(
                compose_file))
            raise SystemExit(1)

    if os.path.exists(windows_file_path):
        docker_compose_cli_args += '{0} '.format(wsl_drive_map(windows_file_path))
    else:
        docker_compose_cli_args += '{0} '.format(cli_arg)

docker_compose_cmd = ['C:\\Windows\\System32\\bash.exe', '-c', '{0} docker-compose {1}'.format(
        bash_variables,
        docker_compose_cli_args
    )
]

# Run the docker-compose binary in bash on WSL with the appropriate argument(s)
docker_compose_process = subprocess.Popen(docker_compose_cmd, shell=True)

try:
    docker_compose_process.wait()
except KeyboardInterrupt:
    docker_compose_process.terminate()

# Python Standard Libraries
import os
import sys
import subprocess
import pathlib

# 3rd party libraries
# import yaml

# Variable(s)
pycharm_compose_override = sys.argv[4] if len(sys.argv) > 3 else ''
default_config = {
    'wsl_drive_map': {
        'C': '/c'
    }
}
docker_compose_cli_args = ' '.join(sys.argv[1:])
bash_variables = ''

# Function(s)
def wsl_drive_map(string_to_map):
    '''
    Replace all the instance of the drive(s) letter(s) to their corresponding WSL mount point

    :param string_to_map:
    :return:
    '''

    for win_drive, wsl_mount in default_config.get('wsl_drive_map').items():
        win_drive = win_drive.upper()
        wsl_mount = '{0}/'.format(wsl_mount) if wsl_mount[-1] != '/' else wsl_mount

        string_to_map = string_to_map \
            .replace('{0}:\\'.format(win_drive), wsl_mount) \
            .replace('{0}:/'.format(win_drive), wsl_mount)

    string_to_map = string_to_map.replace('\\', '/')

    return string_to_map

# Add the docker variable(s), defined in the Windows environment variable(s) to the docker-compose command
for key, value in os.environ.items():
    if key.startswith('DOCKER'):
        if isinstance(value, int):
            bash_variables += '{0}={1} '.format(key, value)
        else:
            bash_variables += '{0}="{1}"'.format(key, value)

# Replace the PyCharm command line option(s) Windows path with WSL path(s)
docker_compose_cli_args = wsl_drive_map(docker_compose_cli_args)
cli_args = ['C:\\Windows\\System32\\bash.exe', '-c', '{0} docker-compose {1}'.format(
        bash_variables,
        docker_compose_cli_args
    )
]

# Replace Windows path with WSL supported path
if os.path.isfile(pycharm_compose_override):
    pycharm_override_content = pathlib.Path(pycharm_compose_override).read_text()
    new_pycharm_override = wsl_drive_map(pycharm_override_content)
    pathlib.Path(pycharm_compose_override).write_text(new_pycharm_override)
else:
    sys.stderr.write('The PyCharm docker-compose override file "{0}" does not exists, exiting...'.format(
        pycharm_compose_override))
    raise SystemExit(1)

print('The docker-compose argument(s) were: {0}'.format(bash_variables))

# Run the docker-compose binary in bash on WSL with the appropriate argument(s)
subprocess.run(cli_args, shell=True)

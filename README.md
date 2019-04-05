# Docker Compose WSL
Use Docker Compose from your Windows Subsystem for Linux (WSL) distribution from PyCharm on Windows

This tool will translate Windows paths, used by the PyCharm IDE, to WSL paths, including the path(s) passed by PyCharm to the docker-compose binary, but also inside the PyCharm docker-compose override file.

## Download

The latest binary can be found on the [release page](https://github.com/stashfiler/docker-compose-wsl/releases)

## Usage in PyCharm

1. Download the [latest binary](https://github.com/stashfiler/docker-compose-wsl/releases)
2. Move the binary to any directory accessible by the PyCharm IDE
3. In PyCharm, go to `File > Settings...`
4. In the `Settings` window, go to `Build, Execution, Deployment > Docker > Tools` and set the **Docker Compose executable** path to the **docker-compose-wsl** binary path

## Remarks

The initial 0.1 release is rough and only support translating the C:\ drive to the /c path inside WSL, but I plan to add support for allowing any drive to be mapped to any WSL path(s), using a YAML configuration file.

## Build from source

1. Download and install the latest [Python 3](https://www.python.org/) interpreter
2. Open a command prompt
3. Install virtualenv

       > pip install virtualenv

4. Create and activate the new virtual environment

       > virtualenv docker-compose-wsl
       > docker-compose-wsl\Scripts\activate

5. Install the dependencies in the virtual environment

       (docker-compose-wsl) > pip install -r requirements.txt

6. Run PyInstaller in order to create the binary

       (docker-compose-wsl) > pyinstaller --onefile .\docker-compose-wsl.py
       
7. The binary will be available in the **dist** directory

## Thanks

* Andy-5 for [WSLGit](https://github.com/andy-5/wslgit) which served as the inspiration for creating this tool
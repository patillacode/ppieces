| Latest Version | Downloads |
|----------------|-----------|
[![PyPI version](https://badge.fury.io/py/ppieces.svg)](https://badge.fury.io/py/ppieces)|[![Downloads](https://pepy.tech/badge/ppieces)](https://pepy.tech/project/ppieces)

# ppieces


### What?

Python Project Creator Script -> PPCS -> PythonPieCeS -> ppieces

`ppieces` is a command-line utility designed to streamline the setup of new Python projects.
It automates various tasks such as creating project directories, initializing git repositories, setting up virtual environments, and installing pre-commit hooks.


### Why?

I tend to always have a python project or two on the go, usually for my own benefit, little scripts to make my day to day easier/faster/automated or just learning new things or experimenting with ideas.

Because of that I found myself repeating the same steps over and over again when setting up new Python projects. *Same song & dance*.

I wanted a way to automate the setup for new projects, so I created `ppieces`.


### Installation

#### Plug & Play:
```bash
# Install via pipx, recommended since you will most likely want to use this tool globally.
pipx install ppieces

# Install via pip, if you prefer to use a virtual environment.
pip install ppieces
```

#### Install for development:

Clone the repository:
```bash
git clone https://github.com/patillacode/ppieces.git
cd ppieces
```

Install the dependencies and the package:
```bash
make install

# or manually:

python -m venv venv
source venv/bin/activate
pip install -e .
```

#### System Requirements

Before using `ppieces`, ensure you have the following installed:

- Python >= `3.10`

Optional:
- `pre-commit` (can be installed via `pipx` or `Homebrew` - see [here](https://pre-commit.com/#install) for more details)
- `autoenv` (optional for auto-activation of virtual environments - see [here](https://github.com/hyperupcall/autoenv?tab=readme-ov-file) for more details)


### Usage

1. Run the `ppieces` script.
2. Follow the interactive prompts to configure your new project.
3. Start coding!

`ppieces` can be used in an interactive mode (by default) or with command-line options for scripting:

Interactive mode will ask you a series of questions to configure your new project.
```bash
$ ppieces
```

https://github.com/patillacode/ppieces/assets/10074977/0a4b4dda-4809-4248-8215-7d4fb0765546


For scripting, use the following options:
```bash
$ ppieces --help

Usage: ppieces [OPTIONS]

Options:
  -ni, --non-interactive     Run the script in non-interactive mode.
  -p, --project-folder PATH  The path to your projects folder.
  -n, --project-name TEXT    The name of the new project.
  -v, --virtual-env          Create a virtual environment.
  -g, --git                  Initialize a git repository (with .gitignore and
                             README files)

  -pre, --pre-commit         Add pre-commit configuration.
  -r, --ruff                 Add a ruff configuration file.
  -a, --autoenv              Set up autoenv.
  -u, --username TEXT        GitHub username to use in README (default: $USER)
  --version                  Show the version of ppieces.
  --help                     Show this message and exit.
```

Example usage:
```bash
ppieces -ni -p /Users/dvitto/projects -n test -v -pre -r -a -g -u patillacode
```


### Features

- **Project Directory Creation**: Automatically creates a new directory for your project.
- **Git Repository Initialization**: Initializes a new git repository in the project directory.
- **Virtual Environment**: Sets up a Python virtual environment within the project.
- **Autoenv Setup**: Configures autoenv to automatically activate the virtual environment when entering the project directory.
- **Ruff Configuration**: Adds a default `.ruff.toml` configuration file for the Ruff static analysis tool.
- **Pre-commit Hooks**: Installs pre-commit hooks to ensure code quality and standards are maintained.
- **Template Files**: Provides template files like `.gitignore`, `requirements.txt`, and `.pre-commit-config.yaml` to get started quickly.


### Acknowledgments

This project makes use of several open-source packages including, but not limited to:
- [`autoenv`](https://github.com/hyperupcall/autoenv?tab=readme-ov-file)
- [`bamp`](https://github.com/inirudebwoy/bamp)
- [`hatch`](https://hatch.pypa.io/latest/)
- [`icecream`](https://github.com/gruns/icecream)
- [`pre-commit`](https://pre-commit.com/)
- [`pyfiglet`](https://github.com/pwaller/pyfiglet)
- [`rich`](https://github.com/Textualize/rich)
- [`termcolor`](https://github.com/termcolor/termcolor)

A big thank you to the maintainers of all these projects and the python and open-source communities in general.


### Contributing

Contributions are welcome!

If you have a feature request, bug report, or a pull request, please open an issue or submit a PR.


### License

`ppieces` is released under the MIT License. See the LICENSE file for more details.


## ppieces

### What?

Python Project Creator Script -> PPCS -> PythonPieCeS -> ppieces

`ppieces` is a command-line utility designed to streamline the setup of new Python projects.
It automates various tasks such as creating project directories, initializing git repositories, setting up virtual environments, and installing pre-commit hooks.

### Command Line Interface (CLI)

`ppieces` can be used in an interactive mode or with command-line options for scripting:

Options:
- `-n`, `--name` project_name: Specify the name of the new project.
- `-v`, `--virtual-env`: Create a virtual environment if given.
- `-pre`, `--pre-commit`: Add pre-commit configuration if given.
- `-r`, `--ruff`: Add a ruff configuration file if given.
- `-a`, `--autoenv`: Set up autoenv if given.
- `-p`, `--project-folder` project_folder_path: Override the `PROJECTS_DIR` from the .env file if given.
- `-i`, `--interactive`: Run the script in interactive mode (default behavior).
- `-g`, `--git`: Initialize a git repository if given.

Example usage:
```bash
ppieces --name my_project --virtual-env --pre-commit --ruff --autoenv --git
```

### Why?

I found myself repeating the same steps over and over again when setting up new Python projects.
I wanted a way to automate these tasks so I could get started on my projects faster.


### Features

- **Project Directory Creation**: Automatically creates a new directory for your project.
- **Git Repository Initialization**: Initializes a new git repository in the project directory.
- **Virtual Environment**: Sets up a Python virtual environment within the project.
- **Autoenv Setup**: Configures autoenv to automatically activate the virtual environment when entering the project directory.
- **Ruff Configuration**: Adds a default `.ruff.toml` configuration file for the Ruff static analysis tool.
- **Pre-commit Hooks**: Installs pre-commit hooks to ensure code quality and standards are maintained.
- **Template Files**: Provides template files like `.gitignore`, `requirements.txt`, and `.pre-commit-config.yaml` to get started quickly.

### Usage

1. Run the `ppieces` script.
2. Follow the interactive prompts to configure your new project.
3. Start coding!

### Requirements

Before using `ppieces`, ensure you have the following installed:

- Python >= 3.10

Optional:
- `pre-commit` (can be installed via pipx or Homebrew - see [here](https://pre-commit.com/#install) for more details)
- `autoenv` (optional for auto-activation of virtual environments - see [here](https://github.com/hyperupcall/autoenv?tab=readme-ov-file) for more details)

### Installation

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/your-username/ppieces.git
cd ppieces
pip install -r requirements.txt
```

### Contributing

Contributions are welcome!

If you have a feature request, bug report, or a pull request, please open an issue or submit a PR.

### License

`ppieces` is released under the MIT License. See the LICENSE file for more details.

### Acknowledgments

This project makes use of several open-source packages such as `pyfiglet`, `termcolor`, `python-dotenv`, `autoenv` and `pre-commit`.

A big thank you to the maintainers of all these projects.

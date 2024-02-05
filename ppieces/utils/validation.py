import os
import re
import subprocess

from rich.console import Console
from termcolor import colored

console = Console()


def validate_projects_folder_path(projects_folder_path):
    msg = None

    if not projects_folder_path:
        msg = colored(
            ("\n\nERROR: You must provide the path to your projects folder."),
            "red",
            attrs=["bold"],
        )
    elif not os.path.exists(projects_folder_path):
        msg = colored(
            (
                f"\n\nERROR: {projects_folder_path} does not exist. "
                "Please provide a valid path."
            ),
            "red",
            attrs=["bold"],
        )

    if msg:
        print(msg)
        exit(1)


def validate_project_name(project_path):
    project_name = os.path.basename(project_path)
    msg = None

    if not project_name:
        msg = colored(
            ("\n\nERROR: You must provide the name of the project."),
            "red",
            attrs=["bold"],
        )

    elif os.path.exists(project_path):
        msg = colored(
            (
                f"\n\nERROR: {project_path} already exists. "
                "Please choose another name or delete the existing folder."
            ),
            "red",
            attrs=["bold"],
        )
    elif not re.match(r"^[a-zA-Z0-9-_]+$", project_name):
        msg = colored(
            (
                "\n\nERROR: Invalid project name. "
                "Project name can only contain letters, numbers, dashes, and underscores."
            ),
            "red",
            attrs=["bold"],
        )

    if msg:
        print(msg)
        exit(1)


def validate_options(
    non_interactive,
    project_folder,
    project_name,
    virtual_env,
    git,
    pre_commit,
    ruff,
    autoenv,
    makefile,
    pip_tools,
    username,
):
    valid = True

    if pre_commit:
        if not git:
            msg = colored(
                (
                    "\nERROR: No point in installing pre-commit without git. "
                    "Please enable the git option if you want to use pre-commit"
                ),
                "red",
                attrs=["bold"],
            )
            print(msg)
            valid = False

        try:
            with console.status("[green]Checking if pre-commit is installed..."):
                subprocess.run(
                    ["pre-commit", "--version"],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
        except Exception:
            msg = colored(
                (
                    "\nWARNING: pre-commit is not installed. Please make sure to install "
                    "it\n\tpipx install pre-commit or brew install pre-commit"
                ),
                "yellow",
                attrs=["bold"],
            )
            print(msg)

            msg = colored(
                ("Continuing without pre-commit. You can install it later.\n"),
                "blue",
                attrs=["bold"],
            )
            print(msg)
            valid = False

    if pip_tools and not virtual_env:
        msg = colored(
            (
                "\nERROR: You shouldn't use pip-tools without a virtual environment. "
                "Please enable the virtual environment option."
            ),
            "red",
            attrs=["bold"],
        )
        print(msg)
        valid = False

    if autoenv and not virtual_env:
        msg = colored(
            (
                "\nERROR: No point in setting autoenv without a virtual "
                "environment. Please enable the virtual environment option."
            ),
            "red",
            attrs=["bold"],
        )
        print(msg)
        valid = False

    if non_interactive and (not project_name or not project_folder):
        msg = colored(
            "\nERROR: Both project name and project folder must be provided when running "
            "in non-interactive mode.\n",
            "red",
            attrs=["bold"],
        )
        print(msg)
        valid = False

    return valid

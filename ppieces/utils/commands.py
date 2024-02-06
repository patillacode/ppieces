import os
import shutil
import subprocess
import sys

import click

from rich.console import Console
from termcolor import colored

from ppieces.utils.constants import SCRIPTS_DIR
from ppieces.utils.copy import (
    copy_gitignore_file,
    copy_pip_tools_requirements_files,
    copy_readme_file,
    copy_requirements_file,
)
from ppieces.utils.prompts import ask_user

console = Console()


def install_precommit_hooks(project_path):
    with console.status("[green]Installing pre-commit hooks..."):
        current_dir = os.getcwd()
        os.chdir(project_path)
        subprocess.run(
            ["pre-commit", "install"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        os.chdir(current_dir)

    msg = colored(
        ("Installed pre-commit hooks successfully!"),
        "cyan",
        attrs=["bold"],
    )
    print(msg)


def setup_autoenv(project_path):
    subprocess.run(
        [os.path.join(f"{SCRIPTS_DIR}", "setup_autoenv.sh"), project_path],
        check=True,
    )
    msg = colored(
        ("Configured autoenv successfully!"),
        "cyan",
        attrs=["bold"],
    )
    print(msg)


def pip_install_requirements(project_path, requirements_file_path="requirements.txt"):
    with console.status("[green]Installing requirements..."):
        subprocess.run(
            [
                f"{project_path}/venv/bin/pip",
                "install",
                "-r",
                os.path.join(project_path, requirements_file_path),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    msg = colored(
        ("Installed requirements successfully!"),
        "cyan",
        attrs=["bold"],
    )
    print(msg)


def add_and_install_requirements(project_path, pip_tools):
    if pip_tools:
        copy_pip_tools_requirements_files(project_path)
        with console.status("[green]Installing pip-tools..."):
            subprocess.run(
                [
                    f"{project_path}/venv/bin/pip",
                    "install",
                    "pip-tools",
                ],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        msg = colored(
            ("Installed pip-tools successfully!"),
            "cyan",
            attrs=["bold"],
        )
        print(msg)

        with console.status("[green]Generating development requirements file..."):
            subprocess.run(
                [
                    f"{project_path}/venv/bin/pip-compile",
                    os.path.join(project_path, "requirements", "development.in"),
                    "--output-file",
                    os.path.join(project_path, "requirements", "development.txt"),
                ],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        msg = colored(
            ("Generated requirement files successfully!"),
            "cyan",
            attrs=["bold"],
        )
        print(msg)
        pip_install_requirements(project_path, "requirements/development.txt")

    else:
        copy_requirements_file(project_path)
        pip_install_requirements(project_path)


def create_virtual_environment(project_path, pip_tools):
    with console.status("[green]Creating virtual environment..."):
        subprocess.run(
            ["python", "-m", "venv", os.path.join(project_path, "venv")], check=True
        )
    msg = colored(
        (f"Created a virtual environment in {project_path}/venv"),
        "cyan",
        attrs=["bold"],
    )
    print(msg)

    with console.status("[green]Upgrading venv pip..."):
        subprocess.run(
            [f"{project_path}/venv/bin/pip", "install", "--upgrade", "pip"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    add_and_install_requirements(project_path, pip_tools)


def initialize_git_repository(project_path, username):
    copy_gitignore_file(project_path)
    copy_readme_file(project_path, username)
    with console.status("[green]Initializing git repo..."):
        subprocess.run(
            ["git", "init", project_path],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    msg = colored(
        ("Initialized git repo successfully!"),
        "cyan",
        attrs=["bold"],
    )
    print(msg)


def initial_commit(project_path):
    with console.status("[green]Creating initial commit..."):
        subprocess.run(
            ["git", "add", "."],
            cwd=project_path,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        subprocess.run(
            ["git", "commit", "-m", "initial commit"],
            cwd=project_path,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    msg = colored(
        ("Created initial commit successfully!"),
        "cyan",
        attrs=["bold"],
    )
    print(msg)


def create_project_directory(project_path):
    try:
        os.makedirs(project_path)
        msg = colored(
            (f"Project directory '{project_path}' created."),
            "yellow",
            attrs=["bold"],
        )
        print(msg)

        return project_path

    except FileExistsError:
        msg = colored(
            (f"\nThe directory '{project_path}' already exists. Aborting."),
            "red",
            attrs=["bold"],
        )
        print(msg)
        msg = colored(
            (
                f"Delete the directory '{project_path}' and try again or give "
                "a different project name.\n"
            ),
            "blue",
            attrs=["bold"],
        )
        print(msg)
        sys.exit(2)


def delete_path(project_path):
    if ask_user(
        colored(
            f"\nDo you want to delete the {project_path} folder to undo any changes done "
            "until now?",
            "red",
            attrs=["bold"],
        )
    ):
        shutil.rmtree(project_path)
        click.echo(
            colored(
                f"{project_path} deleted.",
                "red",
                attrs=["bold"],
            )
        )
        return True

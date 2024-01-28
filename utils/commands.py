import os
import shutil
import subprocess

import click

from rich.console import Console
from termcolor import colored

from utils.constants import SCRIPTS_DIR
from utils.copy import copy_file
from utils.prompts import ask_user

console = Console()


def check_precommit(git):
    if not git:
        msg = colored(
            ("Cannot install pre-commit without git. Ignoring..."),
            "red",
            attrs=["bold"],
        )
        print(msg)
        return False

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
                "pre-commit is not installed. Please make sure to install it\n"
                "pipx install pre-commit or brew install pre-commit"
            ),
            "red",
            attrs=["bold"],
        )
        print(msg)

        msg = colored(
            ("Continuing without pre-commit. You can install it later.\n"),
            "blue",
            attrs=["bold"],
        )
        print(msg)
        return False

    return True


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
        ("Pre-commit hooks installed successfully."),
        "yellow",
        attrs=["bold"],
    )
    print(msg)


def setup_autoenv(project_path):
    subprocess.run(
        [os.path.join(f"./{SCRIPTS_DIR}", "setup_autoenv.sh"), project_path],
        check=True,
    )


def add_and_install_requirements(project_path):
    copy_file("requirements.txt", project_path)

    with console.status("[green]Installing default requirements..."):
        subprocess.run(
            [
                f"{project_path}/venv/bin/pip",
                "install",
                "-r",
                os.path.join(project_path, "requirements.txt"),
                "--upgrade",
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    msg = colored(
        ("Requirements installed successfully."),
        "yellow",
        attrs=["bold"],
    )
    print(msg)


def create_virtual_environment(project_path):
    with console.status("[green]Creating virtual environment..."):
        subprocess.run(
            ["python", "-m", "venv", os.path.join(project_path, "venv")], check=True
        )
    msg = colored(
        (f"Created a virtual environment in {project_path}/venv"),
        "yellow",
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
    add_and_install_requirements(project_path)


def initialize_git_repository(project_path):
    subprocess.run(["git", "init", project_path], check=True)
    copy_file(".gitignore", project_path)


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
                "a different project name."
            ),
            "blue",
            attrs=["bold"],
        )
        print(msg)

        if delete_path(project_path):
            return create_project_directory(project_path)

        raise click.Abort()


def delete_path(project_path):
    if ask_user(f"\nDo you want to delete the {project_path} folder?"):
        shutil.rmtree(project_path)
        click.echo(
            colored(
                f"{project_path} deleted.",
                "red",
                attrs=["bold"],
            )
        )
        return True

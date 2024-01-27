import os
import shutil
import subprocess
import sys

from termcolor import colored

from utils.constants import SCRIPTS_DIR, TEMPLATES_DIR


def check_precommit():
    try:
        msg = colored(
            ("Checking if pre-commit is installed..."),
            "blue",
            attrs=["bold"],
        )
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
    msg = colored(
        ("Installing pre-commit hooks..."),
        "blue",
        attrs=["bold"],
    )
    print(msg)

    current_dir = os.getcwd()
    os.chdir(project_path)
    subprocess.run(
        ["pre-commit", "install"],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    msg = colored(
        ("Pre-commit hooks installed successfully."),
        "yellow",
        attrs=["bold"],
    )
    print(msg)
    os.chdir(current_dir)


def setup_autoenv(project_path):
    subprocess.run(
        [os.path.join(f"./{SCRIPTS_DIR}", "setup_autoenv.sh"), project_path],
        check=True,
    )


def add_and_install_requirements(project_path):
    shutil.copy(
        os.path.join(TEMPLATES_DIR, "requirements.txt"),
        os.path.join(project_path, "requirements.txt"),
    )
    msg = colored(
        (f"Created a default requirements.txt file in {project_path}"),
        "yellow",
        attrs=["bold"],
    )
    print(msg)
    msg = colored(
        ("Installing default requirements..."),
        "blue",
        attrs=["bold"],
    )
    print(msg)
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
    msg = colored(
        ("Creating virtual environment..."),
        "blue",
        attrs=["bold"],
    )
    print(msg)
    subprocess.run(
        ["python", "-m", "venv", os.path.join(project_path, "venv")], check=True
    )
    msg = colored(
        (f"Created a virtual environment in {project_path}/venv"),
        "yellow",
        attrs=["bold"],
    )
    print(msg)
    msg = colored(
        ("Upgrading venv pip..."),
        "blue",
        attrs=["bold"],
    )
    print(msg)

    subprocess.run(
        [f"{project_path}/venv/bin/pip", "install", "--upgrade", "pip"],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    add_and_install_requirements(project_path)


def initialize_git_repository(project_path):
    subprocess.run(["git", "init", project_path], check=True)
    shutil.copy(
        os.path.join(TEMPLATES_DIR, ".gitignore"),
        os.path.join(project_path, ".gitignore"),
    )
    msg = colored(
        (f"Added a default .gitignore to {project_path}."),
        "yellow",
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
            "yellow",
            attrs=["bold"],
        )
        print(msg)
        sys.exit(2)

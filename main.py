#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys

from pyfiglet import Figlet
from termcolor import colored

SCRIPTS_DIR = "scripts"
TEMPLATES_DIR = "templates"
PROJECTS_DIR = "/Users/dvitto/projects"


def welcome():
    os.system("clear")
    # lean isometric1 poison alligator larry3d trek chunky
    fig = Figlet(font="trek")
    print()
    print(colored(fig.renderText(" COOKIE "), "cyan"))
    print(colored(fig.renderText("  CUTTER "), "cyan"))

    welcome_text = colored(
        ("\nWelcome to Cookiecutter, a python project initializer!\n"),
        "red",
        attrs=["bold"],
    )
    print(welcome_text)
    print("-" * len(welcome_text))


def bye():
    msg: str = colored("\nAll set! Happy coding!\n", "red", attrs=["bold"])
    print(msg)


def query_yes_no(question):
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    prompt = " [y/n] "
    default = "yes"
    while True:
        print(colored(f"{question}{prompt}", "cyan", attrs=["bold"]), end="")
        choice = input().lower()
        if choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            msg = colored(
                ("Please respond with 'yes' or 'no' (or 'y' or 'n')."),
                "red",
                attrs=["bold"],
            )
            print(msg)


def create_main_file(project_path):
    shutil.copy(
        os.path.join(TEMPLATES_DIR, "main.py"),
        os.path.join(project_path, "main.py"),
    )
    msg = colored(
        (f"Created a default main.py file in {project_path}"),
        "yellow",
        attrs=["bold"],
    )
    print(msg)


def create_precommit_config(project_path):
    shutil.copy(
        os.path.join(TEMPLATES_DIR, ".pre-commit-config.yaml"),
        os.path.join(project_path, ".pre-commit-config.yaml"),
    )
    msg = colored(
        (f"Created a default .pre-commit-config.yaml file in {project_path}"),
        "yellow",
        attrs=["bold"],
    )
    print(msg)
    # check if pre-commit is installed
    try:
        subprocess.run(
            ["pre-commit", "--version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        msg = colored(
            (
                "pre-commit is not installed. Please install it\n"
                "pipx install pre-commit or brew install pre-commit"
            ),
            "red",
            attrs=["bold"],
        )
        print(msg)
        sys.exit()
    # install pre-commit hooks
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


def create_ruff_config(project_path):
    shutil.copy(
        os.path.join(TEMPLATES_DIR, ".ruff.toml"),
        os.path.join(project_path, ".ruff.toml"),
    )
    msg = colored(
        (f"Created a default .ruff.toml file in {project_path}"),
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
        print()
        msg = colored(
            (f"The directory '{project_path}' already exists. Aborting."),
            "red",
            attrs=["bold"],
        )
        print(msg)
        sys.exit()


def main():
    welcome()
    project_name = input(
        colored("Enter the name of your new project: ", "cyan", attrs=["bold"])
    )
    project_path = os.path.join(PROJECTS_DIR, project_name)

    create_project_directory(project_path)

    if query_yes_no("Do you want to initialize a git repository?"):
        initialize_git_repository(project_path)

    if query_yes_no("Do you want to create a virtual environment?"):
        create_virtual_environment(project_path)

    if query_yes_no("Do you want to set up autoenv?"):
        setup_autoenv(project_path)

    if query_yes_no("Do you want to add a config file for ruff?"):
        create_ruff_config(project_path)

    if query_yes_no("Do you want to add a config file for pre-commit?"):
        create_precommit_config(project_path)

    create_main_file(project_path)

    bye()


if __name__ == "__main__":
    main()

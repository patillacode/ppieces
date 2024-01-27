import os
import shutil
import subprocess
import sys

from dotenv import load_dotenv
from termcolor import colored

from utils.constants import TEMPLATES_DIR

load_dotenv()


def copy_file():
    pass


def copy_main_file(project_path):
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


def copy_precommit_config(project_path):
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


def copy_ruff_config(project_path):
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

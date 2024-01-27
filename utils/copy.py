import os
import shutil

from dotenv import load_dotenv
from termcolor import colored

from utils.constants import TEMPLATES_DIR

load_dotenv()


def copy_file(filename, project_path):
    shutil.copy(
        os.path.join(TEMPLATES_DIR, filename),
        os.path.join(project_path, filename),
    )
    msg = colored(
        (f"Created a default {filename} file in {project_path}"),
        "yellow",
        attrs=["bold"],
    )
    print(msg)


def copy_main_file(project_path):
    copy_file("main.py", project_path)


def copy_precommit_config(project_path):
    copy_file(".pre-commit-config.yaml", project_path)


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

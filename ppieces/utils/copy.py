import os
import shutil

from termcolor import colored

from ppieces.utils.constants import TEMPLATES_DIR


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
    copy_file(".ruff.toml", project_path)

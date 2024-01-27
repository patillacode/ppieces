import os

from dotenv import load_dotenv
from termcolor import colored

from utils.commands import (
    create_project_directory,
    create_virtual_environment,
    initialize_git_repository,
    setup_autoenv,
)
from utils.copy import copy_main_file, copy_precommit_config, copy_ruff_config
from utils.messages import bye, query_yes_no, welcome

load_dotenv()

PROJECTS_DIR = os.getenv("PROJECTS_DIR")


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
        copy_ruff_config(project_path)

    if query_yes_no("Do you want to add a config file for pre-commit?"):
        copy_precommit_config(project_path)

    copy_main_file(project_path)

    bye()


if __name__ == "__main__":
    main()

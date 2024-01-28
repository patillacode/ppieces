import os
import shutil

import click

from termcolor import colored

from utils.commands import (
    check_precommit,
    create_project_directory,
    create_virtual_environment,
    initialize_git_repository,
    install_precommit_hooks,
    setup_autoenv,
)
from utils.copy import copy_main_file, copy_precommit_config, copy_ruff_config
from utils.prompts import ask_user, bye, welcome


def run_cli(
    non_interactive,
    project_folder,
    project_name,
    virtual_env,
    pre_commit,
    ruff,
    autoenv,
    git,
):
    try:
        if non_interactive:
            project_path = os.path.join(project_folder, project_name)
            create_project_directory(project_path)

            if git:
                initialize_git_repository(project_path)

            if virtual_env:
                create_virtual_environment(project_path)

            if autoenv:
                setup_autoenv(project_path)

            if ruff:
                copy_ruff_config(project_path)

            if pre_commit:
                copy_precommit_config(project_path)
                if check_precommit(git):
                    install_precommit_hooks(project_path)

            copy_main_file(project_path)

        else:
            welcome()

            default_projects_folder_path = os.path.join(os.getenv("HOME"), "projects")
            projects_folder_path = input(
                colored(
                    "Enter the absolute path of your projects folder (default: "
                    f"{default_projects_folder_path}): ",
                    "cyan",
                    attrs=["bold"],
                )
            )
            if not projects_folder_path:
                projects_folder_path = default_projects_folder_path

            project_name = input(
                colored("Enter the name of your new project: ", "cyan", attrs=["bold"])
            )
            project_path = os.path.join(projects_folder_path, project_name)

            create_project_directory(project_path)

            if git := ask_user("Do you want to initialize a git repository?"):
                initialize_git_repository(project_path)

            if ask_user("Do you want to create a virtual environment?"):
                create_virtual_environment(project_path)

            if ask_user("Do you want to set up autoenv?"):
                setup_autoenv(project_path)

            if ask_user("Do you want to add a config file for ruff?"):
                copy_ruff_config(project_path)

            if ask_user("Do you want to add a config file for pre-commit?"):
                copy_precommit_config(project_path)
                if check_precommit(git):
                    install_precommit_hooks(project_path)

            copy_main_file(project_path)

            bye()

    except KeyboardInterrupt:
        print(colored("\nAborting...", "red", attrs=["bold"]))
        if project_path and os.path.exists(project_path):
            if click.confirm(
                colored(
                    f"Do you want to delete the {project_path} folder?",
                    "red",
                    attrs=["bold"],
                ),
                default=False,
            ):
                shutil.rmtree(project_path)
                click.echo(
                    colored(
                        f"{project_path} deleted.",
                        "blue",
                        attrs=["bold"],
                    )
                )

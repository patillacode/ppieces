import os

from termcolor import colored

from ppieces.utils.commands import (
    create_project_directory,
    delete_path,
)
from ppieces.utils.flows import finalize_project, get_project_path, setup_project
from ppieces.utils.prompts import ask_user, bye, welcome


def run_cli(
    non_interactive,
    project_folder,
    project_name,
    virtual_env,
    git,
    pre_commit,
    ruff,
    autoenv,
    makefile,
    username,
):
    project_path = None
    try:
        if non_interactive:
            project_path = os.path.join(project_folder, project_name)
            create_project_directory(project_path, interactive=False)

            options = {
                "virtual_env": virtual_env,
                "git": git,
                "autoenv": autoenv,
                "ruff": ruff,
                "pre_commit": pre_commit,
                "makefile": makefile,
            }

        else:
            welcome()
            project_path = get_project_path()
            project_name = os.path.basename(project_path)
            create_project_directory(project_path, interactive=True)

            options = {
                "virtual_env": ask_user(
                    f"Do you want to create a virtual environment for `{project_name}` "
                    "project?"
                ),
                "git": ask_user(
                    f"Do you want to initialize a git repository for `{project_name}` "
                    "project?"
                ),
                "autoenv": ask_user(
                    f"Do you want to autoenv config files for `{project_name}` project?"
                ),
                "ruff": ask_user(
                    f"Do you want to add a ruff config file for `{project_name}` project?"
                ),
                "pre_commit": ask_user(
                    f"Do you want to add a pre-commit config file for `{project_name}` "
                    "project?"
                ),
                "makefile": ask_user(
                    f"Do you want to add a Makefile for `{project_name}` project?"
                ),
            }
            git = options["git"]

        setup_project(project_path, options, username)
        finalize_project(project_path, git, pre_commit)
        bye()

    except KeyboardInterrupt:
        print(colored("\nAborting...", "red", attrs=["bold"]))
        if project_path and os.path.exists(project_path):
            delete_path(project_path)

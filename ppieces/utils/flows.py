import os

from termcolor import colored

from ppieces.utils.commands import (
    check_precommit,
    create_virtual_environment,
    initial_commit,
    initialize_git_repository,
    install_precommit_hooks,
    setup_autoenv,
)
from ppieces.utils.copy import (
    copy_main_file,
    copy_makefile,
    copy_precommit_config,
    copy_ruff_config,
)
from ppieces.utils.validation import validate_project_name, validate_projects_folder_path


def get_project_path():
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

    validate_projects_folder_path(projects_folder_path)

    project_name = input(
        colored("Enter the name of your new project: ", "cyan", attrs=["bold"])
    )
    validate_project_name(project_name)

    return os.path.join(projects_folder_path, project_name)


def setup_project(
    project_path,
    options,
    username,
):
    options_mapping = {
        "virtual_env": create_virtual_environment,
        "git": initialize_git_repository,
        "autoenv": setup_autoenv,
        "ruff": copy_ruff_config,
        "pre_commit": copy_precommit_config,
        "makefile": copy_makefile,
    }

    copy_main_file(project_path)

    for option, value in options.items():
        if value:
            if option == "git":
                options_mapping[option](project_path, username)
            else:
                options_mapping[option](project_path)


def finalize_project(project_path, git):
    # once we know a git repo was initialized, we can install pre-commit hooks
    if check_precommit(git):
        install_precommit_hooks(project_path)

    # otherwise, we inform the user that we can't install pre-commit hooks
    # without a git repo
    else:
        msg = colored(
            ("\n\nWARNING: pre-commit is not installed. " "Please install it manually."),
            "red",
            attrs=["bold"],
        )
        print(msg)

    # this should be the last step since we are making the initial commit
    # AFTER all the template files are copied to the new project folder
    if git:
        initial_commit(project_path)

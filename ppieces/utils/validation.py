import os
import re

from termcolor import colored


def validate_projects_folder_path(projects_folder_path):
    msg = None

    if not projects_folder_path:
        msg = colored(
            ("\n\nERROR: You must provide the path to your projects folder."),
            "red",
            attrs=["bold"],
        )
    elif not os.path.exists(projects_folder_path):
        msg = colored(
            (
                f"\n\nERROR: {projects_folder_path} does not exist. "
                "Please provide a valid path."
            ),
            "red",
            attrs=["bold"],
        )

    if msg:
        print(msg)
        exit(1)


def validate_project_name(project_path):
    project_name = os.path.basename(project_path)
    msg = None

    if not project_name:
        msg = colored(
            ("\n\nERROR: You must provide the name of the project."),
            "red",
            attrs=["bold"],
        )

    elif os.path.exists(project_path):
        msg = colored(
            (
                f"\n\nERROR: {project_path} already exists. "
                "Please choose another name or delete the existing folder."
            ),
            "red",
            attrs=["bold"],
        )
    elif not re.match(r"^[a-zA-Z0-9-_]+$", project_name):
        msg = colored(
            (
                "\n\nERROR: Invalid project name. "
                "Project name can only contain letters, numbers, dashes, and underscores."
            ),
            "red",
            attrs=["bold"],
        )

    if msg:
        print(msg)
        exit(1)

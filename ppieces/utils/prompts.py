import os
import random

from pyfiglet import Figlet
from termcolor import colored

from ppieces.utils.validation import validate_project_name, validate_projects_folder_path

SCRIPTS_DIR = "scripts"
TEMPLATES_DIR = "templates"
PROJECTS_DIR = "/Users/dvitto/projects"


def welcome():
    os.system("clear")
    # isometric1, chunky, poison, cybermedium
    font = random.choice(["lean", "cyberlarge", "alligator", "larry3d", "trek"])
    fig = Figlet(font=font)
    print()
    print(colored(fig.renderText(" ppieces"), "cyan"))

    welcome_text = colored(
        ("\nWelcome to ppieces, a python project initializer!\n"),
        "red",
        attrs=["bold"],
    )
    print(welcome_text)
    print("-" * len(welcome_text))


def bye():
    msg: str = colored("\nAll set! Happy coding!\n", "green", attrs=["bold"])
    print(msg)


def ask_user(question):
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    prompt = " [Y/n] "
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

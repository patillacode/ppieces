import os

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

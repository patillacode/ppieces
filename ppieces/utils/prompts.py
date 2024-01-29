import os
import random

from pyfiglet import Figlet
from termcolor import colored

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
    msg: str = colored("\nAll set! Happy coding!\n", "blue", attrs=["bold"])
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

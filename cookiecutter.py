#!/usr/bin/env python3

import os
import subprocess

def main():
    print("Welcome to Cookiecutter, the Python project initializer!")
    project_name = input("Enter the name of your new project: ")
    create_project_directory(project_name)
    # Additional steps will be implemented here.

def create_project_directory(name):
    try:
        os.makedirs(name)
        print(f"Project directory '{name}' created.")
    except FileExistsError:
        print(f"The directory '{name}' already exists.")

if __name__ == "__main__":
    main()

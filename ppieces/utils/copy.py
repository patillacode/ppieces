import os
import shutil

from termcolor import colored

from ppieces.utils.constants import TEMPLATES_DIR


def copy_template_file(filename, project_path):
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


def copy_requirements_file(project_path):
    copy_template_file("requirements.txt", project_path)


def copy_makefile(project_path):
    copy_template_file("Makefile", project_path)


def copy_main_file(project_path):
    copy_template_file("main.py", project_path)


def copy_precommit_config(project_path):
    copy_template_file(".pre-commit-config.yaml", project_path)


def copy_ruff_config(project_path):
    copy_template_file(".ruff.toml", project_path)


def copy_gitignore_file(project_path):
    copy_template_file(".gitignore", project_path)


def copy_readme_file(project_path, username):
    copy_template_file("README-sample.md", project_path)
    project_name = os.path.basename(project_path)
    with open(os.path.join(project_path, "README-sample.md"), "r") as f:
        readme = f.read()
        readme = readme.replace("{{project_name}}", project_name)
        readme = readme.replace("{{username}}", username)
    with open(os.path.join(project_path, "README-sample.md"), "w") as f:
        f.write(readme)
    os.rename(
        os.path.join(project_path, "README-sample.md"),
        os.path.join(project_path, "README.md"),
    )

import os
import shutil
import subprocess

import click

from termcolor import colored

from utils.cli import run_cli


@click.command()
@click.option(
    "-ni",
    "--non-interactive",
    is_flag=True,
    default=False,
    help="Run the script in non-interactive mode.",
)
@click.option(
    "-p",
    "--project-folder",
    type=click.Path(exists=True),
    required=False,
    help="The path to your projects folder.",
)
@click.option(
    "-n",
    "--project-name",
    type=str,
    required=False,
    help="The name of the new project.",
)
@click.option(
    "-v",
    "--virtual-env",
    is_flag=True,
    help="Create a virtual environment.",
)
@click.option(
    "-pre",
    "--pre-commit",
    is_flag=True,
    help="Add pre-commit configuration.",
)
@click.option(
    "-r",
    "--ruff",
    is_flag=True,
    help="Add a ruff configuration file.",
)
@click.option(
    "-a",
    "--autoenv",
    is_flag=True,
    help="Set up autoenv.",
)
@click.option(
    "-g",
    "--git",
    is_flag=True,
    help="Initialize a git repository.",
)
def main(
    project_folder,
    project_name,
    virtual_env,
    pre_commit,
    ruff,
    autoenv,
    non_interactive,
    git,
):
    try:
        if non_interactive and not project_name and not project_folder:
            raise click.UsageError(
                "The project name and project folder must be provided when running in "
                "non-interactive mode."
            )

        run_cli(
            non_interactive,
            project_folder,
            project_name,
            virtual_env,
            pre_commit,
            ruff,
            autoenv,
            git,
        )
    except KeyboardInterrupt:
        print(colored("\n\nKeyboard interrupt detected.", "red", attrs=["bold"]))
        if project_folder and project_name and os.path.exists(project_folder):
            if click.confirm(
                f"Do you want to delete the {project_folder}/{project_name}?",
                default=False,
            ):
                shutil.rmtree(os.path.join(project_folder, project_name))
                click.echo(
                    colored(
                        f"{project_folder}/{project_name} deleted.",
                        "yellow",
                        attrs=["bold"],
                    )
                )
    except subprocess.CalledProcessError as err:
        print(colored(err, "red", attrs=["bold"]))
        print(colored("Aborting...", "red", attrs=["bold"]))
        if project_folder and project_name and os.path.exists(project_folder):
            shutil.rmtree(os.path.join(project_folder, project_name))
            click.echo(
                colored(
                    f"Cleaning up after error: {project_folder}/{project_name} deleted.",
                    "yellow",
                    attrs=["bold"],
                )
            )


if __name__ == "__main__":
    main()

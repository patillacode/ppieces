import os
import sys

import click

from termcolor import colored

from ppieces.utils.cli import run_cli
from ppieces.utils.validation import validate_options
from ppieces.version import __version__


@click.command()
@click.option(
    "-ni",
    "--non-interactive",
    is_flag=True,
    default=False,
    help="Run the script in non-interactive mode.",
)
@click.option(
    "-f",
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
    "-g",
    "--git",
    is_flag=True,
    help="Initialize a git repository (with .gitignore and README files)",
)
@click.option(
    "-c",
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
    "-m",
    "--makefile",
    is_flag=True,
    help="Add a default Makefile.",
)
@click.option(
    "-p",
    "--pip-tools",
    is_flag=True,
    help="Add a default pip-tools setups.",
)
@click.option(
    "-u",
    "--username",
    type=str,
    required=False,
    default=os.getenv("USER"),
    help="GitHub username to use in README (default: $USER)",
)
@click.option(
    "--version",
    is_flag=True,
    help="Show the version of ppieces.",
)
def main(
    non_interactive,
    project_folder,
    project_name,
    virtual_env,
    git,
    pre_commit,
    ruff,
    autoenv,
    makefile,
    pip_tools,
    username,
    version,
):
    if version:
        click.echo(__version__)
        sys.exit(1)

    if not validate_options(
        non_interactive,
        project_folder,
        project_name,
        virtual_env,
        git,
        pre_commit,
        ruff,
        autoenv,
        makefile,
        pip_tools,
        username,
    ):
        click.echo(
            colored(
                "\nTry 'ppieces --help' for help.\n",
                "cyan",
                attrs=["bold"],
            )
        )
        sys.exit(2)

    run_cli(
        non_interactive,
        project_folder,
        project_name,
        virtual_env,
        git,
        pre_commit,
        ruff,
        autoenv,
        makefile,
        pip_tools,
        username,
    )


if __name__ == "__main__":  # pragma: no cover
    main()

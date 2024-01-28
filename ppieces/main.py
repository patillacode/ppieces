import click

from ppieces.utils.cli import run_cli


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


if __name__ == "__main__":
    main()

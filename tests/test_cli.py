import pytest

from click.testing import CliRunner

from ppieces.main import main
from ppieces.version import __version__


@pytest.fixture
def runner():
    return CliRunner()


def test_ctrl_c(runner, mocker, tmp_path):
    fake_projects_folder = tmp_path / "fake/folder"
    fake_projects_folder.mkdir(parents=True, exist_ok=True)
    fake_project = fake_projects_folder / "fake_project"
    mocker.patch("ppieces.utils.flows.setup_project", return_value=None)
    mocker.patch("ppieces.utils.flows.finalize_project", return_value=None)
    mocker.patch(
        "builtins.input",
        side_effect=[
            fake_projects_folder,
            fake_project,
            KeyboardInterrupt,
            "y",
        ],
    )
    result = runner.invoke(main)
    print(result.output)
    print(result.exception)
    assert result.exit_code == 0
    assert "Aborting..." in result.output


def test_cli_version(runner):
    result = runner.invoke(main, ["--version"])
    assert __version__ in result.output


def test_cli_help(runner):
    result = runner.invoke(main, ["--help"])
    assert "Usage: main [OPTIONS]" in result.output
    assert "--help" in result.output


def test_cli_non_interactive_with_piptools(runner, mocker, tmp_path):
    mocker.patch("ppieces.utils.commands.create_project_directory", return_value=None)
    mocker.patch("ppieces.utils.flows.setup_project", return_value=None)
    mocker.patch("ppieces.utils.flows.finalize_project", return_value=None)
    mocker.patch("ppieces.utils.commands.initial_commit", return_value=None)
    fake_projects_folder = tmp_path / "fake/folder"
    fake_projects_folder.mkdir(parents=True, exist_ok=True)
    fake_project = fake_projects_folder / "fake_project"

    result = runner.invoke(
        main,
        [
            "--non-interactive",
            f"--project-folder={fake_projects_folder}",
            "--project-name=fake_project",
            "--virtual-env",
            "--git",
            "--pre-commit",
            "--ruff",
            "--autoenv",
            "--makefile",
            "--pip-tools",
            "--username=fake_user",
        ],
    )
    print(result.output)
    print(result.exception)
    assert result.exit_code == 0

    # check for the directory and the files that should be created
    assert (fake_project).exists()
    assert (fake_project / ".git").exists()
    assert (fake_project / ".gitignore").exists()
    assert (fake_project / ".pre-commit-config.yaml").exists()
    assert (fake_project / ".ruff.toml").exists()
    assert (fake_project / ".autoenv.sh").exists()
    assert (fake_project / ".autoenv_leave.sh").exists()
    assert (fake_project / "requirements").exists()
    assert (fake_project / "requirements" / "development.txt").exists()
    assert (fake_project / "requirements" / "base.in").exists()
    assert (fake_project / "requirements" / "test.in").exists()
    assert (fake_project / "requirements" / "production.in").exists()
    assert (fake_project / "requirements" / "development.in").exists()
    assert (fake_project / "venv").exists()
    assert (fake_project / "README.md").exists()
    assert (fake_project / "Makefile").exists()
    assert (fake_project / "main.py").exists()


def test_cli_interactive(runner, mocker, tmp_path):
    fake_projects_folder = tmp_path / "fake/folder"
    fake_projects_folder.mkdir(parents=True, exist_ok=True)
    fake_project = fake_projects_folder / "fake_project"
    mocker.patch("ppieces.utils.flows.setup_project", return_value=None)
    mocker.patch("ppieces.utils.flows.finalize_project", return_value=None)
    mocker.patch(
        "builtins.input",
        side_effect=[
            fake_projects_folder,
            fake_project,
            "y",
            "y",
            "y",
            "y",
            "y",
            "y",
            "y",
            "y",
        ],
    )
    result = runner.invoke(main)
    assert result.exit_code == 0
    # check for the directory and the files that should be created
    assert (fake_project).exists()
    assert (fake_project / ".git").exists()
    assert (fake_project / ".gitignore").exists()
    assert (fake_project / ".pre-commit-config.yaml").exists()
    assert (fake_project / ".ruff.toml").exists()
    assert (fake_project / ".autoenv.sh").exists()
    assert (fake_project / ".autoenv_leave.sh").exists()
    assert (fake_project / "requirements").exists()
    assert (fake_project / "requirements" / "development.txt").exists()
    assert (fake_project / "requirements" / "base.in").exists()
    assert (fake_project / "requirements" / "test.in").exists()
    assert (fake_project / "requirements" / "production.in").exists()
    assert (fake_project / "requirements" / "development.in").exists()
    assert (fake_project / "venv").exists()
    assert (fake_project / "README.md").exists()
    assert (fake_project / "Makefile").exists()
    assert (fake_project / "main.py").exists()

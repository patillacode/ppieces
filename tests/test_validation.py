import pytest

from click.testing import CliRunner

from ppieces.main import main
from ppieces.utils.validation import validate_project_name, validate_projects_folder_path


@pytest.fixture
def runner():
    return CliRunner()


def test_missing_project_folder(runner):
    result = runner.invoke(
        main,
        [
            "--non-interactive",
        ],
    )
    assert result.exit_code == 2
    assert (
        "Both project name and project folder must be provided when running "
        "in non-interactive mode"
    ) in result.output


def test_missing_project_name(runner, tmp_path):
    fake_projects_folder = tmp_path / "fake/folder"
    fake_projects_folder.mkdir(parents=True, exist_ok=True)
    result = runner.invoke(
        main,
        [
            "--non-interactive",
            f"--project-folder={fake_projects_folder}",
        ],
    )
    assert result.exit_code == 2
    assert (
        "Both project name and project folder must be provided when running "
        "in non-interactive mode"
    ) in result.output


def test_pre_commit_without_git(runner, tmp_path):
    fake_projects_folder = tmp_path / "fake/folder"
    fake_projects_folder.mkdir(parents=True, exist_ok=True)
    result = runner.invoke(
        main,
        [
            "--non-interactive",
            f"--project-folder={fake_projects_folder}",
            "--project-name=fake_project",
            "--pre-commit",
        ],
    )
    assert result.exit_code == 2
    assert ("No point in installing pre-commit without git") in result.output


def test_pre_commit_wit_git(runner, mocker, tmp_path):
    mocker.patch("ppieces.utils.validation.subprocess.run", return_value=0)
    fake_projects_folder = tmp_path / "fake/folder"
    fake_projects_folder.mkdir(parents=True, exist_ok=True)
    result = runner.invoke(
        main,
        [
            "--non-interactive",
            f"--project-folder={fake_projects_folder}",
            "--project-name=fake_project",
            "--pre-commit",
            "--git",
        ],
    )
    assert result.exit_code == 0


def test_pre_commit_is_not_installed(runner, mocker, tmp_path):
    mocker.patch("ppieces.utils.validation.subprocess.run", side_effect=Exception)

    fake_projects_folder = tmp_path / "fake/folder"
    fake_projects_folder.mkdir(parents=True, exist_ok=True)
    result = runner.invoke(
        main,
        [
            "--non-interactive",
            f"--project-folder={fake_projects_folder}",
            "--project-name=fake_project",
            "--pre-commit",
            "--git",
        ],
    )
    assert result.exit_code == 2
    assert (
        "WARNING: pre-commit is not installed. Please make sure to install"
    ) in result.output
    assert ("Continuing without pre-commit. You can install it later.") in result.output


def test_pip_tools_without_virtual_env(runner, tmp_path):
    fake_projects_folder = tmp_path / "fake/folder"
    fake_projects_folder.mkdir(parents=True, exist_ok=True)
    result = runner.invoke(
        main,
        [
            "--non-interactive",
            f"--project-folder={fake_projects_folder}",
            "--project-name=fake_project",
            "--pip-tools",
        ],
    )
    assert result.exit_code == 2
    assert (
        "You shouldn't use pip-tools without a virtual environment. "
        "Please enable the virtual environment option."
    ) in result.output


def test_autoenv_without_virtual_env(runner, tmp_path):
    fake_projects_folder = tmp_path / "fake/folder"
    fake_projects_folder.mkdir(parents=True, exist_ok=True)
    result = runner.invoke(
        main,
        [
            "--non-interactive",
            f"--project-folder={fake_projects_folder}",
            "--project-name=fake_project",
            "--autoenv",
        ],
    )
    assert result.exit_code == 2
    assert (
        "No point in setting autoenv without a virtual environment. "
        "Please enable the virtual environment option."
    ) in result.output


def test_validate_projects_folder_path_missing(runner, mocker):
    with pytest.raises(SystemExit) as pytest_wrapped_exception:
        validate_projects_folder_path("")
    assert pytest_wrapped_exception.type == SystemExit
    assert pytest_wrapped_exception.value.code == 1


def test_validate_projects_folder_path_nonexistent(runner, mocker):
    with pytest.raises(SystemExit) as pytest_wrapped_exception:
        validate_projects_folder_path("/nonexistent/path")
    assert pytest_wrapped_exception.type == SystemExit
    assert pytest_wrapped_exception.value.code == 1


def test_validate_project_name_empty(runner, mocker):
    with pytest.raises(SystemExit) as pytest_wrapped_exception:
        validate_project_name("")
    assert pytest_wrapped_exception.type == SystemExit
    assert pytest_wrapped_exception.value.code == 1


def test_validate_project_name_existing(runner, mocker, tmp_path):
    existing_project_path = tmp_path / "existing_project"
    existing_project_path.mkdir()
    with pytest.raises(SystemExit) as pytest_wrapped_exception:
        validate_project_name(str(existing_project_path))
    assert pytest_wrapped_exception.type == SystemExit
    assert pytest_wrapped_exception.value.code == 1


def test_validate_project_name_invalid_characters(runner, mocker):
    with pytest.raises(SystemExit) as pytest_wrapped_exception:
        validate_project_name("inval!d/pr#ject/nam^")
    assert pytest_wrapped_exception.type == SystemExit
    assert pytest_wrapped_exception.value.code == 1

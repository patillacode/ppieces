import os
import subprocess

from unittest.mock import call, mock_open

import pytest

from ppieces.utils import commands


@pytest.fixture
def mock_subprocess_run(mocker):
    return mocker.patch("subprocess.run", autospec=True)


@pytest.fixture
def mock_os_chdir(mocker):
    return mocker.patch("os.chdir", autospec=True)


@pytest.fixture
def mock_os_makedirs(mocker):
    return mocker.patch("os.makedirs", autospec=True)


@pytest.fixture
def mock_shutil_rmtree(mocker):
    return mocker.patch("shutil.rmtree", autospec=True)


def test_install_precommit_hooks(mock_subprocess_run, mock_os_chdir):
    project_path = "/fake/project/path"
    commands.install_precommit_hooks(project_path)
    calls = [call(project_path), call(os.getcwd())]
    mock_os_chdir.assert_has_calls(calls)
    mock_subprocess_run.assert_called_with(
        ["pre-commit", "install"],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def test_setup_autoenv(mock_subprocess_run):
    project_path = "/fake/project/path"
    commands.setup_autoenv(project_path)
    mock_subprocess_run.assert_called_with(
        [os.path.join(commands.SCRIPTS_DIR, "setup_autoenv.sh"), project_path],
        check=True,
    )


def test_pip_install_requirements(mock_subprocess_run):
    project_path = "/fake/project/path"
    requirements_file_path = "requirements.txt"
    commands.pip_install_requirements(project_path, requirements_file_path)
    mock_subprocess_run.assert_called_with(
        [
            f"{project_path}/venv/bin/pip",
            "install",
            "-r",
            os.path.join(project_path, requirements_file_path),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def test_create_virtual_environment(mock_subprocess_run, mocker):
    mock_add_and_install_requirements = mocker.patch(
        "ppieces.utils.commands.add_and_install_requirements"
    )
    project_path = "/fake/project/path"
    commands.create_virtual_environment(project_path, False)
    calls = [
        call(["python", "-m", "venv", os.path.join(project_path, "venv")], check=True),
        call(
            [f"{project_path}/venv/bin/pip", "install", "--upgrade", "pip"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ),
    ]
    mock_subprocess_run.assert_has_calls(calls)
    mock_add_and_install_requirements.assert_called_once_with(project_path, False)


def test_initialize_git_repository(mock_subprocess_run, mocker):
    mocker.patch("ppieces.utils.copy.copy_gitignore_file")
    mocker.patch("ppieces.utils.copy.copy_readme_file")
    mocker.patch("ppieces.utils.copy.copy_template_file")
    mocker.patch("builtins.open", mock_open())
    mocker.patch("os.rename")
    project_path = "/fake/project/path"
    username = "fakeuser"
    commands.initialize_git_repository(project_path, username)
    calls = [
        call(["git", "init", project_path], check=True, stdout=-3, stderr=-3),
    ]
    mock_subprocess_run.assert_has_calls(calls)


def test_initial_commit(mock_subprocess_run):
    project_path = "/fake/project/path"
    commands.initial_commit(project_path)
    calls = [
        call(
            ["git", "add", "."],
            cwd=project_path,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ),
        call(
            ["git", "commit", "-m", "initial commit"],
            cwd=project_path,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ),
    ]
    mock_subprocess_run.assert_has_calls(calls)


def test_create_project_directory(mock_os_makedirs):
    project_path = "/fake/project/path"
    commands.create_project_directory(project_path)
    mock_os_makedirs.assert_called_with(project_path)


def test_add_and_install_requirements_with_pip_tools(
    mock_subprocess_run, mocker, tmp_path
):
    project_path = tmp_path / "fake_project"
    project_path.mkdir()
    mocker.patch("ppieces.utils.copy.copy_pip_tools_requirements_files")
    commands.add_and_install_requirements(str(project_path), True)
    calls = [
        call(
            [f"{project_path}/venv/bin/pip", "install", "pip-tools"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ),
        call(
            [
                f"{project_path}/venv/bin/pip-compile",
                os.path.join(project_path, "requirements", "development.in"),
                "--output-file",
                os.path.join(project_path, "requirements", "development.txt"),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ),
    ]
    mock_subprocess_run.assert_has_calls(calls)


def test_add_and_install_requirements_without_pip_tools(
    mock_subprocess_run, mocker, tmp_path
):
    project_path = tmp_path / "fake_project"
    project_path.mkdir()
    mocker.patch("ppieces.utils.copy.copy_requirements_file")
    commands.add_and_install_requirements(project_path, False)
    mock_subprocess_run.assert_called_once_with(
        [
            f"{project_path}/venv/bin/pip",
            "install",
            "-r",
            os.path.join(project_path, "requirements.txt"),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def test_create_project_directory_existing_dir(mock_os_makedirs):
    project_path = "/fake/project/path"
    mock_os_makedirs.side_effect = FileExistsError
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        commands.create_project_directory(project_path)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2
    mock_os_makedirs.assert_called_with(project_path)


def test_delete_path(mock_shutil_rmtree, mocker):
    project_path = "/fake/project/path"
    mocker.patch("ppieces.utils.prompts.ask_user", return_value=True)
    mocker.patch("builtins.input", return_value="yes")
    assert commands.delete_path(project_path) is True
    mock_shutil_rmtree.assert_called_with(project_path)


def test_delete_path_negative(mock_shutil_rmtree, mocker):
    project_path = "/fake/project/path"
    mocker.patch("ppieces.utils.prompts.ask_user", return_value=False)
    mocker.patch("builtins.input", return_value="no")
    assert commands.delete_path(project_path) is None
    mock_shutil_rmtree.assert_not_called()

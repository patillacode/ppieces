import os

from unittest.mock import mock_open

import pytest

from ppieces.utils import copy


# Tests for the copy module will be added here.
@pytest.fixture
def mock_shutil_copy(mocker):
    return mocker.patch("shutil.copy", autospec=True)


@pytest.fixture
def mock_os_path_join(mocker):
    return mocker.patch("os.path.join", autospec=True)


@pytest.fixture
def mock_print(mocker):
    return mocker.patch("builtins.print", autospec=True)


def test_copy_template_file(mock_shutil_copy, mock_os_path_join, mock_print):
    filename = "sample.txt"
    project_path = "/fake/project/path"
    copy.copy_template_file(filename, project_path)
    mock_os_path_join.assert_called_with(project_path, filename)
    mock_shutil_copy.assert_called_with(
        mock_os_path_join.return_value, os.path.join(project_path, filename)
    )
    mock_print.assert_called()


def test_copy_requirements_file(mock_shutil_copy, mock_os_path_join, mock_print):
    project_path = "/fake/project/path"
    copy.copy_requirements_file(project_path)
    mock_os_path_join.assert_called_with(project_path, "requirements.txt")
    mock_shutil_copy.assert_called_with(
        mock_os_path_join.return_value, os.path.join(project_path, "requirements.txt")
    )
    mock_print.assert_called()


def test_copy_makefile(mock_shutil_copy, mock_os_path_join, mock_print):
    project_path = "/fake/project/path"
    pip_tools = False
    copy.copy_makefile(project_path, pip_tools)
    mock_os_path_join.assert_called_with(project_path, "Makefile")
    mock_shutil_copy.assert_called_with(
        mock_os_path_join.return_value, os.path.join(project_path, "Makefile")
    )
    mock_print.assert_called()


def test_copy_pip_tools_requirements_files(
    mock_shutil_copy, mock_os_path_join, mock_print, mocker
):
    project_path = "/fake/project/path"
    mocker.patch(
        "glob.glob",
        return_value=["/fake/templates/pip-tools/requirements/development.in"],
    )
    mocker.patch("os.makedirs", autospec=True)
    copy.copy_pip_tools_requirements_files(project_path)
    mock_os_path_join.assert_called_with(project_path, "requirements")
    mock_shutil_copy.assert_called()
    mock_print.assert_called()


def test_copy_main_file(mock_shutil_copy, mock_os_path_join, mock_print):
    project_path = "/fake/project/path"
    copy.copy_main_file(project_path)
    mock_os_path_join.assert_called_with(project_path, "main.py")
    mock_shutil_copy.assert_called_with(
        mock_os_path_join.return_value, os.path.join(project_path, "main.py")
    )
    mock_print.assert_called()


def test_copy_precommit_config(mock_shutil_copy, mock_os_path_join, mock_print):
    project_path = "/fake/project/path"
    copy.copy_precommit_config(project_path)
    mock_os_path_join.assert_called_with(project_path, ".pre-commit-config.yaml")
    mock_shutil_copy.assert_called_with(
        mock_os_path_join.return_value,
        os.path.join(project_path, ".pre-commit-config.yaml"),
    )
    mock_print.assert_called()


def test_copy_ruff_config(mock_shutil_copy, mock_os_path_join, mock_print):
    project_path = "/fake/project/path"
    copy.copy_ruff_config(project_path)
    mock_os_path_join.assert_called_with(project_path, ".ruff.toml")
    mock_shutil_copy.assert_called_with(
        mock_os_path_join.return_value, os.path.join(project_path, ".ruff.toml")
    )
    mock_print.assert_called()


def test_copy_gitignore_file(mock_shutil_copy, mock_os_path_join, mock_print):
    project_path = "/fake/project/path"
    copy.copy_gitignore_file(project_path)
    mock_os_path_join.assert_called_with(project_path, ".gitignore")
    mock_shutil_copy.assert_called_with(
        mock_os_path_join.return_value, os.path.join(project_path, ".gitignore")
    )
    mock_print.assert_called()


def test_copy_readme_file(mock_shutil_copy, mock_os_path_join, mock_print, mocker):
    project_path = "/fake/project/path"
    username = "fakeuser"
    mocker.patch(
        "builtins.open",
        mock_open(read_data="Project name: {{project_name}}\nUsername: {{username}}"),
    )
    mocker.patch("os.rename", autospec=True)
    copy.copy_readme_file(project_path, username)
    mock_os_path_join.assert_called_with(project_path, "README.md")
    mock_shutil_copy.assert_called_with(
        mock_os_path_join.return_value, os.path.join(project_path, "README-sample.md")
    )
    mock_print.assert_called()
    open.assert_called_with(os.path.join(project_path, "README-sample.md"), "w")
    os.rename.assert_called_with(
        os.path.join(project_path, "README-sample.md"),
        os.path.join(project_path, "README.md"),
    )

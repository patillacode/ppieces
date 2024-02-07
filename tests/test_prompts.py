import os

import pytest

from ppieces.utils import prompts


@pytest.fixture
def mock_input(mocker):
    return mocker.patch("builtins.input", side_effect=[""])


@pytest.fixture
def mock_print(mocker):
    return mocker.patch("builtins.print")


@pytest.fixture
def mock_os_system(mocker):
    return mocker.patch("os.system")


def test_welcome(mock_os_system, mock_print):
    prompts.welcome()
    mock_os_system.assert_called_once_with("clear")
    assert mock_print.call_count > 0


def test_bye(mock_print):
    prompts.bye()
    mock_print.assert_called_once()


def test_ask_user_yes(mock_input, mock_print):
    mock_input.side_effect = ["y"]
    assert prompts.ask_user("Is this a test?") is True


def test_ask_user_no(mock_input, mock_print):
    mock_input.side_effect = ["n"]
    assert prompts.ask_user("Is this a test?") is False


def test_ask_user_default_yes(mock_input, mock_print):
    mock_input.side_effect = [""]
    assert prompts.ask_user("Is this a test?") is True


def test_ask_user_invalid_input(mock_input, mock_print):
    mock_input.side_effect = ["maybe", "y"]
    assert prompts.ask_user("Is this a test?") is True
    assert mock_print.call_count == 3


def test_get_project_path_default(mock_input, mocker):
    mock_input.side_effect = ["", "test_project"]
    mocker.patch("ppieces.utils.prompts.validate_projects_folder_path")
    mocker.patch("ppieces.utils.prompts.validate_project_name")
    expected_path = os.path.join(os.getenv("HOME"), "projects", "test_project")
    assert prompts.get_project_path() == expected_path


def test_get_project_path_custom(mock_input, mocker):
    custom_path = "/custom/projects"
    mock_input.side_effect = [custom_path, "test_project"]
    mocker.patch("ppieces.utils.prompts.validate_projects_folder_path")
    mocker.patch("ppieces.utils.prompts.validate_project_name")
    expected_path = os.path.join(custom_path, "test_project")
    assert prompts.get_project_path() == expected_path

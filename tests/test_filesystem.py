import pytest

from app.tools.filesystem import (
    get_allowed_directories,
    list_directory,
    search_files
)


def test_allowed_directories():

    directories = get_allowed_directories()

    assert isinstance(directories, dict)


def test_downloads_access():

    directories = get_allowed_directories()

    if "Downloads" not in directories:
        pytest.skip("Downloads directory does not exist")

    result = list_directory("~/Downloads")

    assert result["success"] is True


def test_system_directory_blocked():

    with pytest.raises(PermissionError):

        list_directory("/System")

def test_search_files():

    result = search_files(
        "~/Downloads",
        "*",
        10
    )

    assert result["success"] is True
    assert "results" in result
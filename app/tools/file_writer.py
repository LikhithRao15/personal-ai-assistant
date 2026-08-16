from pathlib import Path

from app.tools.filesystem import resolve_allowed_path


MAX_WRITE_SIZE = 2 * 1024 * 1024  # 2 MB


def create_directory(path: str):

    directory = resolve_allowed_path(path)

    if directory.exists():

        if directory.is_dir():
            return {
                "success": True,
                "created": False,
                "message": "Directory already exists.",
                "path": str(directory)
            }

        return {
            "success": False,
            "error": "A file already exists at this path."
        }

    try:

        directory.mkdir(
            parents=True,
            exist_ok=False
        )

        return {
            "success": True,
            "created": True,
            "path": str(directory),
            "message": "Directory created successfully."
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error)
        }


def write_file(path: str, content: str):

    file_path = resolve_allowed_path(path)

    if len(content.encode("utf-8")) > MAX_WRITE_SIZE:

        return {
            "success": False,
            "error": "Content exceeds the 2 MB write limit."
        }

    if file_path.exists() and file_path.is_dir():

        return {
            "success": False,
            "error": "Cannot write content to a directory."
        }

    try:

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        file_path.write_text(
            content,
            encoding="utf-8"
        )

        return {
            "success": True,
            "path": str(file_path),
            "bytes_written": file_path.stat().st_size,
            "message": "File written successfully."
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error)
        }
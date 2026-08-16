from pathlib import Path

from app.tools.filesystem import resolve_allowed_path


MAX_FILE_SIZE = 2 * 1024 * 1024  # 2 MB

SUPPORTED_EXTENSIONS = {
    ".txt",
    ".md",
    ".py",
    ".json",
    ".csv",
}


def read_file(path: str):

    file_path = resolve_allowed_path(path)

    if not file_path.exists():
        return {
            "success": False,
            "error": "File does not exist."
        }

    if not file_path.is_file():
        return {
            "success": False,
            "error": "Path is not a file."
        }

    extension = file_path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        return {
            "success": False,
            "error": (
                f"Unsupported file type: {extension}. "
                f"Supported types: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
            )
        }

    size = file_path.stat().st_size

    if size > MAX_FILE_SIZE:
        return {
            "success": False,
            "error": "File is larger than the 2 MB reading limit."
        }

    try:

        content = file_path.read_text(
            encoding="utf-8",
            errors="replace"
        )

        return {
            "success": True,
            "path": str(file_path),
            "size_bytes": size,
            "content": content
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error)
        }
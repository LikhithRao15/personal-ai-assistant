from pathlib import Path


HOME = Path.home()

ALLOWED_DIRECTORIES = {
    "home":Path.home(),
    "Desktop": HOME / "Desktop",
    "Documents": HOME / "Documents",
    "Downloads": HOME / "Downloads",
}


def get_allowed_directories():
    return {
        name: str(path)
        for name, path in ALLOWED_DIRECTORIES.items()
        if path.exists()
    }


def resolve_allowed_path(path: str) -> Path:
    """
    Resolve a path and make sure it stays inside an allowed directory.
    """

    requested = Path(path).expanduser().resolve()

    for allowed in ALLOWED_DIRECTORIES.values():

        allowed = allowed.resolve()

        try:
            requested.relative_to(allowed)
            return requested
        except ValueError:
            continue

    raise PermissionError(
        f"Access denied: {requested}"
    )


def list_directory(path: str):
    directory = resolve_allowed_path(path)

    if not directory.exists():
        return {
            "success": False,
            "error": "Directory does not exist."
        }

    if not directory.is_dir():
        return {
            "success": False,
            "error": "Path is not a directory."
        }

    items = []

    for item in directory.iterdir():

        items.append({
            "name": item.name,
            "type": "directory" if item.is_dir() else "file"
        })

    return {
        "success": True,
        "path": str(directory),
        "items": items
    }

def search_files(
    directory: str,
    pattern: str = "*",
    max_results: int = 100
):
    """
    Search recursively inside an allowed directory.

    Examples:
        *.pdf
        *.py
        resume*
        *
    """

    root = resolve_allowed_path(directory)

    if not root.exists():
        return {
            "success": False,
            "error": "Directory does not exist."
        }

    if not root.is_dir():
        return {
            "success": False,
            "error": "Search path is not a directory."
        }

    results = []

    for item in root.rglob(pattern):

        if not item.is_file():
            continue

        try:
            size = item.stat().st_size

            results.append({
                "name": item.name,
                "path": str(item),
                "size_bytes": size
            })

        except OSError:
            continue

        if len(results) >= max_results:
            break

    return {
        "success": True,
        "directory": str(root),
        "pattern": pattern,
        "count": len(results),
        "results": results
    }
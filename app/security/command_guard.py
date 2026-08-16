import shlex


SAFE_COMMANDS = {
    "pwd",
    "ls",
    "echo",
    "whoami",
    "date",
    "uname",
    "python",
    "python3",
    "pytest",
    "git",
    "node",
    "npm",
    "pip",
    "pip3",
}


DANGEROUS_COMMANDS = {
    "rm",
    "rmdir",
    "sudo",
    "shutdown",
    "reboot",
    "mkfs",
    "diskutil",
}


def get_base_command(command: str) -> str | None:

    try:

        parts = shlex.split(command)

        if not parts:
            return None

        return parts[0].split("/")[-1]

    except ValueError:

        return None


def classify_command(command: str) -> str:

    base = get_base_command(command)

    if base is None:
        return "blocked"

    if base in DANGEROUS_COMMANDS:
        return "dangerous"

    if base in SAFE_COMMANDS:
        return "safe"

    return "moderate"
import subprocess
from pathlib import Path

from app.security.terminal_policy import check_command
from app.tools.filesystem import resolve_allowed_path


MAX_OUTPUT = 12000
DEFAULT_TIMEOUT = 30


def execute_command(
    command: str,
    working_directory: str = "~",
    timeout: int = DEFAULT_TIMEOUT,
    confirmed: bool = False,
):
    """
    Execute a terminal command after passing through
    the NEXUS command safety policy.

    Commands requiring confirmation will NOT execute unless
    confirmed=True is supplied by the application layer.
    """

    if not command.strip():
        return {
            "success": False,
            "error": "Command cannot be empty."
        }

    policy = check_command(command)

    if policy["classification"] == "blocked":

        return {
            "success": False,
            "classification": "blocked",
            "error": policy["reason"],
        }

    if policy["requires_confirmation"] and not confirmed:

        return {
            "success": False,
            "requires_confirmation": True,
            "classification": policy["classification"],
            "command": command,
            "error": policy["reason"],
        }

    try:

        cwd = resolve_allowed_path(
            working_directory
        )

        if not cwd.exists():
            return {
                "success": False,
                "error": "Working directory does not exist."
            }

        if not cwd.is_dir():
            return {
                "success": False,
                "error": "Working directory is not a directory."
            }

        result = subprocess.run(
            command,
            shell=True,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        stdout = result.stdout or ""
        stderr = result.stderr or ""

        output = stdout

        if stderr:
            output += "\n[stderr]\n" + stderr

        if len(output) > MAX_OUTPUT:
            output = (
                output[:MAX_OUTPUT]
                + "\n\n[Output truncated]"
            )

        return {
            "success": result.returncode == 0,
            "return_code": result.returncode,
            "command": command,
            "working_directory": str(cwd),
            "output": output,
        }

    except subprocess.TimeoutExpired:

        return {
            "success": False,
            "error": f"Command timed out after {timeout} seconds."
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error)
        }
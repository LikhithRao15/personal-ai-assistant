import subprocess


def open_application(application_name: str):

    if not application_name:
        raise ValueError("Application name is required.")

    result = subprocess.run(
        ["open", "-a", application_name],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:

        error = result.stderr.strip()

        return {
            "success": False,
            "application": application_name,
            "error": error or "Unable to open application."
        }

    return {
        "success": True,
        "application": application_name,
        "message": f"{application_name} opened successfully."
    }
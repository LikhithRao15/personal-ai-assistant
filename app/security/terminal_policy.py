from app.security.command_guard import classify_command


def check_command(command: str):

    classification = classify_command(command)

    if classification == "blocked":

        return {
            "allowed": False,
            "requires_confirmation": False,
            "classification": "blocked",
            "reason": "Command could not be safely parsed."
        }

    if classification == "dangerous":

        return {
            "allowed": False,
            "requires_confirmation": True,
            "classification": "dangerous",
            "reason": (
                "This command can potentially modify or "
                "damage the system."
            )
        }

    if classification == "moderate":

        return {
            "allowed": False,
            "requires_confirmation": True,
            "classification": "moderate",
            "reason": (
                "This command is not on the trusted "
                "safe-command list."
            )
        }

    return {
        "allowed": True,
        "requires_confirmation": False,
        "classification": "safe",
        "reason": "Command is allowed."
    }
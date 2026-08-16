import json

from app.security.confirmation import ConfirmationManager


class ToolExecutor:

    def __init__(self, registry):

        self.registry = registry
        self.confirmation = ConfirmationManager()

    def execute(self, tool_call):

        tool_name = tool_call.name

        try:

            arguments = json.loads(
                tool_call.arguments or "{}"
            )

            # Terminal commands require an application-level
            # confirmation before execution.
            if tool_name == "terminal_execute":

                command = arguments.get(
                    "command",
                    ""
                )

                from app.security.terminal_policy import (
                    check_command
                )

                policy = check_command(command)

                if policy["requires_confirmation"]:

                    approved = self.confirmation.ask(
                        command,
                        policy["classification"],
                        policy["reason"]
                    )

                    if not approved:

                        result = {
                            "success": False,
                            "cancelled": True,
                            "message": (
                                "The user denied execution "
                                "of this command."
                            )
                        }

                    else:

                        arguments["confirmed"] = True

                        result = self.registry.execute(
                            tool_name,
                            arguments
                        )

                else:

                    result = self.registry.execute(
                        tool_name,
                        arguments
                    )

            else:

                result = self.registry.execute(
                    tool_name,
                    arguments
                )

            return {
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": json.dumps(
                    result,
                    default=str
                )
            }

        except Exception as error:

            return {
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": json.dumps({
                    "success": False,
                    "error": str(error)
                })
            }
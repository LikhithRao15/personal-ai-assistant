import json


class ToolExecutor:

    def __init__(self, registry):
        self.registry = registry

    def execute(self, tool_call):

        try:
            arguments = json.loads(
                tool_call.arguments or "{}"
            )

            result = self.registry.execute(
                tool_call.name,
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
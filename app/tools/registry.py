from typing import Callable, Dict, Any


class ToolRegistry:

    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}

    def register(
        self,
        name: str,
        description: str,
        function: Callable
    ):
        self.tools[name] = {
            "name": name,
            "description": description,
            "function": function
        }

    def get(self, name: str):
        return self.tools.get(name)

    def list_tools(self):
        return list(self.tools.values())

    def execute(self, name: str, arguments: dict | None = None):

        tool = self.get(name)

        if not tool:
            raise ValueError(f"Tool '{name}' not found.")

        if arguments is None:
            arguments = {}

        return tool["function"](**arguments)
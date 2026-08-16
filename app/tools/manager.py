from app.tools.registry import ToolRegistry
from app.tools.system import get_system_info
from app.tools.applications import open_application


def create_tool_registry():

    registry = ToolRegistry()

    registry.register(
        name="system_info",
        description=(
            "Get information about the Mac including operating system, "
            "architecture, processor, RAM and disk usage."
        ),
        function=get_system_info
    )

    registry.register(
        name="open_application",
        description=(
            "Open an installed macOS application by its application name."
        ),
        function=open_application
    )

    return registry
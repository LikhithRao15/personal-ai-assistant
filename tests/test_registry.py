from app.tools.manager import create_tool_registry


def test_system_tool_registered():

    registry = create_tool_registry()

    tool = registry.get("system_info")

    assert tool is not None
    assert tool["name"] == "system_info"


def test_system_tool_execution():

    registry = create_tool_registry()

    result = registry.execute("system_info")

    assert "system" in result
    assert "machine" in result
    assert "memory_total_gb" in result
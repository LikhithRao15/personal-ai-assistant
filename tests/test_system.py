from app.tools.system import get_system_info


def test_system_info():

    result = get_system_info()

    assert "system" in result
    assert "machine" in result
    assert "memory_total_gb" in result
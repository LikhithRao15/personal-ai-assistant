from enum import Enum


class PermissionLevel(Enum):

    SAFE = "safe"
    MODERATE = "moderate"
    DANGEROUS = "dangerous"
    CRITICAL = "critical"


TOOL_PERMISSIONS = {

    "system_info": PermissionLevel.SAFE,

    "open_application": PermissionLevel.SAFE,

    "search_files": PermissionLevel.SAFE,

    "read_file": PermissionLevel.SAFE,

    "create_file": PermissionLevel.MODERATE,

    "move_file": PermissionLevel.MODERATE,

    "copy_file": PermissionLevel.MODERATE,

    "terminal_execute": PermissionLevel.DANGEROUS,

    "delete_file": PermissionLevel.DANGEROUS,

}

def get_permission_level(tool_name: str):

    return TOOL_PERMISSIONS.get(
        tool_name,
        PermissionLevel.CRITICAL
    )


def requires_confirmation(tool_name: str):

    level = get_permission_level(tool_name)

    return level in {
        PermissionLevel.DANGEROUS,
        PermissionLevel.CRITICAL
    }
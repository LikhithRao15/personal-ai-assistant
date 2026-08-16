import platform
import psutil


def get_system_info():

    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    return {
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "memory_total_gb": round(memory.total / (1024 ** 3), 2),
        "memory_used_percent": memory.percent,
        "disk_total_gb": round(disk.total / (1024 ** 3), 2),
        "disk_used_percent": disk.percent,
    }
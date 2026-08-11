from app.config import settings

MAINTENANCE_MODE = settings.MAINTENANCE


def is_maintenance() -> bool:
    return MAINTENANCE_MODE


def set_maintenance(value: bool):
    global MAINTENANCE_MODE
    MAINTENANCE_MODE = value

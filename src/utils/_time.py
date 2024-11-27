from src.localization import get_localizator


_ = get_localizator("time")


def seconds_to_hms(seconds: int) -> str:
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours}{_('_hours')} {minutes}{_('_minutes')} {seconds}{_('_seconds')}"
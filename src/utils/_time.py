from datetime import datetime
import pytz

from src.localization import get_localizator


_ = get_localizator("time")


def seconds_to_hms(seconds: int) -> str:
    """
    Args:
        seconds (int)

    Returns:
        str: `23h 59m 59s`
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return (f"{hours}{_('_hours')} "
            f"{minutes}{_('_minutes')} "
            f"{seconds}{_('_seconds')}")


def current_time() -> datetime:
    """
    Returns:
        datetime: tz = 'Europe/Moscow'
    """

    tz = pytz.timezone('Europe/Moscow')
    return datetime.now(tz)

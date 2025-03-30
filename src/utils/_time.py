from disnake.utils import format_dt

from datetime import datetime, time, date, timedelta
from typing import Optional, Union
import pytz

from src.localization import get_localizator


_ = get_localizator("time")


def seconds_to_hms(seconds: int) -> str:
    """
    Args:
        seconds (int): The number of seconds.

    Returns:
        str: A formatted string representing the time in hours, minutes, and seconds.\
        `[Example: 23h 59m 59s]`
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    parts = []
    if hours: parts.append(f"{hours}{_('_hours')}")
    if minutes: parts.append(f"{minutes}{_('_minutes')}")
    if seconds > 0: parts.append(f"{seconds}{_('_seconds')}")

    return " ".join(parts)


def current_time() -> datetime:
    """
    Returns:
        datetime: tz = 'Europe/Moscow'
    """

    tz = pytz.timezone('Europe/Moscow')
    return datetime.now(tz)


def string_to_datetime(date_string: str) -> datetime:
    """
    Args:
        time_string (str): A formatted string in 1999-01-01T23:59:59.99999 format.

    Returns:
        datetime: Date in datetime format.
    """
    return datetime.fromisoformat(date_string.replace('Z', '+00:00'))


def string_to_timedelta(time_string: str) -> timedelta:
    """
    Args:
        time_string (str): A formatted string in HH:MM:SS format.

    Returns:
        timedelta: Time in timedelta format.
    """
    time_object = datetime.strptime(time_string, "%H:%M:%S").time()
    zero_time = time(0, 0, 0)
    combined = datetime.combine(date.today(), time_object)
    zero_combined = datetime.combine(date.today(), zero_time)
    return combined - zero_combined


def hms_time_string(time_string: str) -> Optional[str]:
    """
    Args:
        time_string (str): A formatted string in HH:MM:SS format.

    Returns:
        str: Combined string_to_timedelta() and seconds_to_hms() result.
    """
    td = string_to_timedelta(time_string)
    if td: return seconds_to_hms(int(td.total_seconds()))

    return None


def make_discord_timestamp(
    dt: Union[datetime, float],
    style: str = 'f'
) -> str:
    """
    Args:
        dt: (datetime | float)
        style (str): The style to format the datetime with. Defaults to `f`
    
    Returns:
        str: A formatted string for discord display. `Example: <t:1618953630:f>`
    """
    return format_dt(dt, style) # type: ignore
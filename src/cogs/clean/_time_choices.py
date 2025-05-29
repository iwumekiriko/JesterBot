from enum import Enum
from datetime import datetime, timedelta

from src.localization import get_localizator


_ = get_localizator("clean.common")


class TimeChoices(str, Enum):
    LAST_HOUR = "last_hour"
    LAST_SIX_HOURS = "last_six_hours"
    LAST_DAY = "last_day"

    def get_time(self) -> datetime:
        now = datetime.now()
        time_deltas = {
            self.LAST_HOUR: timedelta(hours=1),
            self.LAST_SIX_HOURS: timedelta(hours=6),
            self.LAST_DAY: timedelta(days=1),
        }
        return now - time_deltas[self]
    
    @property
    def translated_name(self) -> str:
        return _(self.value + '_choice')
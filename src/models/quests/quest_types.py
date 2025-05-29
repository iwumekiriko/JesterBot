from enum import Enum

from src.localization import get_localizator


_ = get_localizator("general.quests-config")


class QuestTypes(str, Enum):
    DAILY = 1
    WEEKLY = 2
    EVENT = 3

    def get_translated_name(self) -> str:
        return {
            QuestTypes.DAILY: _("quests-config-time_types-daily_name"),
            QuestTypes.WEEKLY: _("quests-config-time_types-weekly_name"),
            QuestTypes.EVENT: _("quests-config-time_types-event_name")
        }[self]

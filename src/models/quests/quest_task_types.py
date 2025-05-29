from enum import Enum

from src.localization import get_localizator


_ = get_localizator("general.quests-config")


class QuestTaskTypes(str, Enum):
    MESSAGES = 1
    VOICE = 2

    def get_translated_name(self) -> str:
        return {
            QuestTaskTypes.MESSAGES: _("quests-config-task_types-messages_name"),
            QuestTaskTypes.VOICE: _("quests-config-task_types-voice_name"),
        }[self]

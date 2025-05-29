from functools import lru_cache
from typing import Dict
import hashlib

from .quest_task_types import QuestTaskTypes
from .quest_reward_types import QuestRewardTypes
from src.localization import get_localizator

_ = get_localizator("general.quests-config")


class QuestsConfig:
    LOCALIZATION_VARIANTS = 8

    titles: Dict[QuestTaskTypes, str] = {
        QuestTaskTypes.MESSAGES: "quests-config-messages_title",
        QuestTaskTypes.VOICE: "quests-config-voice_title"
    }
    descriptions: Dict[QuestTaskTypes, str] = {
        QuestTaskTypes.MESSAGES: "quests-config-messages_desc",
        QuestTaskTypes.VOICE: "quests-config-voice_desc"
    }
    assets: Dict[QuestTaskTypes, Dict[str, str]] = {
        QuestTaskTypes.MESSAGES: {
            "thumbnail": "https://i.imgur.com/xKICzua.jpeg",
            "embed_color": "0x7f159c"
        },
        QuestTaskTypes.VOICE: {
            "thumbnail": "https://i.imgur.com/xKICzua.jpeg",
            "embed_color": "0x16bb32"
        },
    }

    @lru_cache()
    @staticmethod
    def get_seed(id: int) -> int:
        r_bytes = str(id).encode()
        hash_obj = hashlib.md5(r_bytes)
        hash_int = int.from_bytes(hash_obj.digest(), byteorder='big')

        return hash_int % QuestsConfig.LOCALIZATION_VARIANTS + 1

    @staticmethod
    def get_desc(quest_task_type: QuestTaskTypes, id: int) -> str:
        return _(f"{QuestsConfig.descriptions[quest_task_type]}_{QuestsConfig.get_seed(id)}")

    @staticmethod
    def get_task_desc(quest_task_type: QuestTaskTypes, required: int, progress: int, channel_id: int) -> str:
        task_desc = _("quests-config-task_desc",
                        task=quest_task_type.get_translated_name(),
                        required=required,
                        progress=progress)
        if channel_id: task_desc += f"\n{_('quests-config-channel_id_condition', channel_id=channel_id)}"
        if progress >= required: task_desc = f"~~{task_desc}~~ *({_('quests-config-completed_quest_string')})*"

        return task_desc

    @staticmethod
    def get_reward_string(reward_type: QuestRewardTypes, reward_amount: int, guild_id: int) -> str:
        return _("quests-config-reward_string",
                 reward_type=reward_type.get_currency_emoji(guild_id), reward_amount=reward_amount)
    
    @staticmethod
    def get_title(quest_task_type: QuestTaskTypes, id: int) -> str:
        return _(f"{QuestsConfig.titles[quest_task_type]}_{QuestsConfig.get_seed(id)}")

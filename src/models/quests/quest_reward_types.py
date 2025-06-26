from enum import Enum

from src.localization import get_localizator
from src.utils.enums import Currency


_ = get_localizator("general.quests-config")


class QuestRewardTypes(str, Enum):
    COINS = 1
    CRYSTALS = 2
    LOOTBOX_KEY = 3
    CARDS_PACK = 4

    def get_translated_name(self) -> str:
        return {
            QuestRewardTypes.COINS: _("quests-config-reward_types-coins_name"),
            QuestRewardTypes.CRYSTALS: _("quests-config-reward_types-crystalls_name"),
            QuestRewardTypes.LOOTBOX_KEY: _("quests-config-reward_types-lootbox_key_name"),
            QuestRewardTypes.CARDS_PACK: _("quests-config-reward_types-cards_pack_name")
        }[self]

    def get_reward_emoji(self, guild_id: int) -> str:
        return {
            QuestRewardTypes.COINS: Currency.COINS.get_icon(guild_id),
            QuestRewardTypes.CRYSTALS: Currency.CRYSTALS.get_icon(guild_id),
            QuestRewardTypes.LOOTBOX_KEY: f"🎟️ (*{_('quests-config-reward_types-lootbox_key_name').lower()}*)",
            QuestRewardTypes.CARDS_PACK: f"🃏 (*{_('quests-config-reward_types-cards_pack_name').lower()}*)"
        }[self]

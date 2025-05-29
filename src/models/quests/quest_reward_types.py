from enum import Enum

from src.localization import get_localizator


_ = get_localizator("general.quests-config")


class QuestRewardTypes(str, Enum):
    COINS = 1
    CRYSTALLS = 2
    LOOTBOX_KEY = 3

    def get_translated_name(self) -> str:
        return {
            QuestRewardTypes.COINS: _("quests-config-reward_types-coins_name"),
            QuestRewardTypes.CRYSTALLS: _("quests-config-reward_types-crystalls_name"),
            QuestRewardTypes.LOOTBOX_KEY: _("quests-config-reward_types-lootbox_key_name")
        }[self]

    def get_currency_emoji(self, guild_id: int) -> str:
        from src.config import cfg

        economy_cfg = cfg.economy_cfg(guild_id)
        return {
            QuestRewardTypes.COINS: economy_cfg.default_currency_icon,
            QuestRewardTypes.CRYSTALLS: economy_cfg.donate_currency_icon,
            QuestRewardTypes.LOOTBOX_KEY: f"🎟️ (*{_('quests-config-reward_types-lootbox_key_name').lower()}*)"
        }[self]

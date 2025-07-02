from enum import Enum

from src.localization import get_localizator
from src.customisation import (
    GUILD_DEF_CURRENCY_NAME,
    GUILD_DEF_CURRENCY_SHORT_NAME,
    GUILD_DONATE_CURRENCY_NAME,
    GUILD_DONATE_CURRENCY_SHORT_NAME
)

_ = get_localizator("general.enums")


class Currency(str, Enum):
    COINS = "coins"
    CRYSTALS = "crystals"

    @property
    def translated(self) -> str:
        return _({
            Currency.COINS: "currency-coins_name",
            Currency.CRYSTALS: "currency-crystals_name"
        }[self])

    def get_icon(self, guild_id: int) -> str:
        from src.config import cfg
        economy_cfg = cfg.economy_cfg(guild_id)

        return {
            Currency.COINS: economy_cfg.default_currency_icon,
            Currency.CRYSTALS: economy_cfg.donate_currency_icon
        }[self]
    
    @property
    def name(self) -> str:
        return {
            Currency.COINS: GUILD_DEF_CURRENCY_NAME,
            Currency.COINS: GUILD_DONATE_CURRENCY_NAME
        }[self]
    
    @property
    def short_name(self) -> str:
        return {
            Currency.COINS: GUILD_DEF_CURRENCY_SHORT_NAME,
            Currency.CRYSTALS: GUILD_DONATE_CURRENCY_SHORT_NAME
        }[self]
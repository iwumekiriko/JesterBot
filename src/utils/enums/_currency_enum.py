from enum import Enum

from src.localization import get_localizator


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
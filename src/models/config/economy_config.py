from dataclasses import dataclass

from .base_config import BaseConfig


@dataclass
class EconomyConfig(BaseConfig):
    default_currency_icon: str = ""
    donate_currency_icon: str = ""
    daily_bonus: int = 0

    def to_dict(self) -> dict:
        return {
            "guildId": self.guild_id,
            "defaultCurrencyIcon": self.default_currency_icon,
            "donateCurrencyIcon": self.default_currency_icon,
            "dailyBonus": self.daily_bonus
        }
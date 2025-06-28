from dataclasses import dataclass

from .base_config import BaseConfig


@dataclass
class PacksConfig(BaseConfig):
    packs_price: int | None = None

    def to_dict(self) -> dict:
        return {
            "guildId": self.guild_id,
            "packsPrice": self.packs_price,
        }
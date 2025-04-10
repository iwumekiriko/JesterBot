from dataclasses import dataclass

from .base_config import BaseConfig
from ..lootboxes import LootboxTypes


@dataclass
class LootboxesConfig(BaseConfig):
    roles_lootbox_key_price: int | None = None
    backgrounds_lootbox_key_price: int | None = None
    active_lootboxes: str | None = None

    def to_dict(self) -> dict:
        return {
            "guildId": self.guild_id,
            "rolesLootboxKeyPrice": self.roles_lootbox_key_price,
            "backgroundsLootboxKeyPrice": self.backgrounds_lootbox_key_price,
            "activeLootboxes": self.active_lootboxes
        }

    def get_price(self, type: LootboxTypes) -> int:
        return {
            LootboxTypes.ROLES_LOOTBOX: self.roles_lootbox_key_price,
            LootboxTypes.BACKGROUNDS_LOOTBOX: self.backgrounds_lootbox_key_price
        }[type] or 3000
from dataclasses import dataclass
from typing import Dict

from src.models.inventory_items.lootbox_key import LootboxKey

from .shop_item import ShopItem
from ..lootboxes import LootboxTypes


@dataclass
class ShopKey(ShopItem):
    lootbox_type: LootboxTypes
    exclusive: bool

    def to_dict(self) -> Dict:
        return {
            "guildId": self.guild_id,
            "guild": self.guild,
            "type": self.lootbox_type,
            "exclusive": self.exclusive,
        }

    @property
    def inventory_item(self) -> LootboxKey:
        return LootboxKey(
            self.guild_id,
            self.guild,
            1, 0,
            self.lootbox_type
        )

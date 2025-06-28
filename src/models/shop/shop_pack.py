from dataclasses import dataclass
from typing import Dict

from src.models.inventory_items.pack import Pack

from .shop_item import ShopItem


@dataclass
class ShopPack(ShopItem):
    id: int
    name: str
    amount: int

    def to_dict(self) -> Dict:
        return {
            "guildId": self.guild_id,
            "guild": self.guild,
            "id": self.id,
            "name": self.name,
            "amount": self.amount
        }

    @property
    def inventory_item(self) -> Pack:
        return Pack(
            self.guild_id,
            self.guild,
            1, 
            self.id,
            self.name
        )

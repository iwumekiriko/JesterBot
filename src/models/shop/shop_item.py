from dataclasses import dataclass
from typing import Optional

from ..guild import Guild
from ..inventory_items.item import Item


@dataclass
class ShopItem:
    guild_id: int
    guild: Optional[Guild]

    @property
    def inventory_item(self) -> Item:
        raise NotImplementedError
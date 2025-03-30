from dataclasses import dataclass
from typing import Optional

from .item import Item
from .items_config import ItemsConfig


@dataclass
class Coin(Item):
    """
    A helper class for handling lootboxes.
    * Not used in inventory.
    """
    amount: Optional[int]

    @property
    def description(self) -> str:
        from src.config import cfg
        icon = cfg.economy_cfg(self.guild_id).default_currency_icon

        return ItemsConfig.get_formatted_desc(
            self.name, amount=self.amount, currency=icon)
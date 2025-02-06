from dataclasses import dataclass
from typing import Optional

from .item import Item


@dataclass
class Coin(Item):
    """
    A helper class for handling lootboxes.
    * Not used in inventory.
    """
    amount: Optional[int]
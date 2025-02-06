from dataclasses import dataclass
from enum import Enum

from .item import Item


class LootboxTypes(Enum):
    ROLES_LOOTBOX = 1
    BACKGROUNDS_LOOTBOX = 2


@dataclass
class LootboxKey(Item):
    lootbox_key_id: int
    type: LootboxTypes
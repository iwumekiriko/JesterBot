from abc import ABC
from dataclasses import dataclass
from typing import Optional

from ..guild import Guild
from ..asset import Asset


@dataclass
class Item(ABC):
    guild_id: int
    guild: Optional[Guild]

    description: Optional[str]
    lootbox_gif: Optional[Asset]
    item_thumbnail: Optional[Asset]
    embed_color: Optional[str]

    count: Optional[int]


    @property
    def name(self) -> str:
        return self.__class__.__name__.lower()
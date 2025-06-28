from abc import ABC
from dataclasses import dataclass
from typing import Optional

from ..guild import Guild
from .items_config import ItemsConfig


@dataclass
class Item(ABC):
    guild_id: int
    guild: Optional[Guild]
    quantity: int

    @property
    def classname_lower(self) -> str:
        return self.classname.lower()

    @property
    def classname(self) -> str:
        return self.__class__.__name__

    @property
    def description(self) -> str:
        raise NotImplementedError

    @property
    def translated_name(self) -> str:
        return ItemsConfig.get_translated_name(self.classname_lower)

    @property
    def lootbox_gif(self) -> Optional[str]:
        return ItemsConfig.assets.get(self.classname, {}).get("lootbox_gif")

    @property
    def thumbnail(self) -> Optional[str]:
        return ItemsConfig.assets.get(self.classname, {}).get("thumbnail")

    @property
    def embed_color(self) -> Optional[str]:
        return ItemsConfig.assets.get(self.classname, {}).get("embed_color")
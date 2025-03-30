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
    def name_lower(self) -> str:
        return self.name.lower()
    
    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def description(self) -> str:
        raise NotImplementedError

    @property
    def lootbox_gif(self) -> Optional[str]:
        return ItemsConfig.assets.get(self.name, {}).get("lootbox_gif")
    
    @property
    def thumbnail(self) -> Optional[str]:
        return ItemsConfig.assets.get(self.name, {}).get("thumbnail")
    
    @property
    def embed_color(self) -> Optional[str]:
        return ItemsConfig.assets.get(self.name, {}).get("embed_color")
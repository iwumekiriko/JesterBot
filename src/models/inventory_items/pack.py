from dataclasses import dataclass

from .item import Item
from .items_config import ItemsConfig

@dataclass
class Pack(Item):
    pack_id: int
    pack_name: str

    @property
    def description(self) -> str:
        return ItemsConfig.get_formatted_desc(
            self.name, name=self.pack_name)
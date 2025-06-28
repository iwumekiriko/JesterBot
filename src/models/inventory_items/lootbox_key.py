from dataclasses import dataclass

from .item import Item
from .items_config import ItemsConfig
from ..lootboxes import LootboxTypes

@dataclass
class LootboxKey(Item):
    lootbox_key_id: int
    type: LootboxTypes

    @property
    def description(self) -> str:
        return ItemsConfig.get_formatted_desc(
            self.classname, type=self.type.translated.lower())
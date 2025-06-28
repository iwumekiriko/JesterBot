from dataclasses import dataclass

from .item import Item
from .items_config import ItemsConfig

from src.localization import get_localizator


_ = get_localizator("general.items-config")


@dataclass
class Pack(Item):
    id: int
    name: str
    quantity: int

    @property
    def description(self) -> str:
        return ItemsConfig.get_formatted_desc(
            self.classname, name=self.name)

    @property
    def formatted_name(self) -> str:
        return _("items-config-pack_formatted_name", name=self.name)
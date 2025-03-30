from enum import Enum
from typing import List

from src.localization import get_localizator
from .types import BaseLootbox
from src.models.lootboxes.lootbox_types import LootboxTypes


_ = get_localizator("lootboxes")


class LootboxMap(str, Enum):
    ROLES_LOOTBOX = "roles"
    # BACKGROUNDS_LOOTBOX = "backgrounds"

    def get_type(self) -> type[BaseLootbox]:
        from .types import RolesLootbox, BackgroundsLootbox

        return {
            LootboxMap.ROLES_LOOTBOX: RolesLootbox,
            # LootboxMap.BACKGROUNDS_LOOTBOX: BackgroundsLootbox
        }[self]

    def get_translated_name(self) -> str:
        return _({
            LootboxMap.ROLES_LOOTBOX: "lootboxes-roles_lootbox_name",
            # LootboxMap.BACKGROUNDS_LOOTBOX: "lootboxes-backgrounds_lootbox_name"
        }[self])

    def get_lootbox_type(self) -> LootboxTypes:
        return {
            LootboxMap.ROLES_LOOTBOX: LootboxTypes.ROLES_LOOTBOX,
            # LootboxMap.BACKGROUNDS_LOOTBOX: LootboxTypes.BACKGROUNDS_LOOTBOX
        }[self]

    @staticmethod
    def lootboxes_with_roles() -> List['LootboxMap']:
        return [LootboxMap.ROLES_LOOTBOX]

from enum import Enum

from src.localization import get_localizator


_ = get_localizator("items-config")


class LootboxTypes(Enum):
    ROLES_LOOTBOX = 1
    BACKGROUNDS_LOOTBOX = 2

    @property
    def translated(self) -> str:
        return {
            LootboxTypes.ROLES_LOOTBOX: _("items-config-roles_lootbox_type_name"),
            LootboxTypes.BACKGROUNDS_LOOTBOX: _("items-config-backgrounds_lootbox_type_name")
        }[self]

from enum import Enum

from src.localization import get_localizator


_ = get_localizator("lootboxes")


class LootboxRolesActions(str, Enum):
    ADD = "add"
    REMOVE = "remove"

    def get_translated_name(self) -> str:
        return _({
            LootboxRolesActions.ADD: "lootboxes-roles-add_action_name",
            LootboxRolesActions.REMOVE: "lootboxes-roles-remove_action_name"
        }[self])

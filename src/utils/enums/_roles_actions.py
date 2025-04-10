from enum import Enum

from src.localization import get_localizator


_ = get_localizator("enums")


class RolesActions(str, Enum):
    ADD = "add"
    REMOVE = "remove"

    def get_translated_name(self) -> str:
        return _({
            RolesActions.ADD: "roles-actions-add_name",
            RolesActions.REMOVE: "roles-actions-remove_name"
        }[self])

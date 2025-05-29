from enum import Enum

from src.localization import get_localizator


_ = get_localizator("general.enums")


class Actions(str, Enum):
    ADD = "add"
    REMOVE = "remove"

    def get_translated_name(self) -> str:
        return _({
            Actions.ADD: "actions-add_name",
            Actions.REMOVE: "actions-remove_name"
        }[self])

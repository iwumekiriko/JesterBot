from dataclasses import dataclass

from .setting_types import SettingTypes


@dataclass
class Setting:
    id: int
    cost: int
    bought: bool
    state: bool
    type: SettingTypes

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "cost": self.cost,
            "bought": self.bought,
            "state": self.state,
            "type": self.type.value
        }
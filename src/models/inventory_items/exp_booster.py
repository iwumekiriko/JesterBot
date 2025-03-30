from dataclasses import dataclass

from .items_config import ItemsConfig
from .item import Item
from src.utils._time import seconds_to_hms


@dataclass
class ExpBooster(Item):
    exp_booster_id: int
    value: int
    duration: int

    @property
    def description(self) -> str:
        return ItemsConfig.get_formatted_desc(
            self.name, value=self.value, duration=self.hms_duration)
    
    @property
    def hms_duration(self) -> str:
        return seconds_to_hms(self.duration)
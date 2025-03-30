from dataclasses import dataclass
from datetime import datetime

from ..user import User
from .item import Item
from src.utils._time import seconds_to_hms


@dataclass
class ActiveExpBooster(Item):
    user_id: int
    user: User
    value: int
    duration: int
    activated_at: datetime | float
    
    @property
    def description(self) -> str:
        return ""
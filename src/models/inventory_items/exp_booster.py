from dataclasses import dataclass
from datetime import timedelta
from typing import Optional

from .item import Item


@dataclass
class ExpBooster(Item):
    exp_booster_id: int
    value: int
    duration: Optional[timedelta]
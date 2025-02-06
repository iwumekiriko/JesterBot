from datetime import timedelta
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from .item import Item


class RoleTypes(Enum):
    SHOP_ROLE = 1
    LOOTBOX_ROLE = 2


@dataclass
class Role(Item):
    role_id: int
    member_role_id: int
    type: RoleTypes
    price: Optional[int]
    duration: Optional[timedelta]
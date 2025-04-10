from dataclasses import dataclass

from ..guild import Guild
from ..user import User


@dataclass
class ShopRoleTries:
    guild_id: int
    guild: Guild
    user_id: int
    user: User
    guild_role_id: int
    tries_used: int
    try_activated: int
    active: bool
from dataclasses import dataclass
from typing import Optional

from ..guild import Guild
from ..user import User
from .setting import Setting


@dataclass
class UserSettings:
    guild_id: int
    guild: Optional[Guild]
    user_id: int
    user: Optional[User]
    settings: list[Setting]
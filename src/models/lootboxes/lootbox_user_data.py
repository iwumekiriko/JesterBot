from dataclasses import dataclass
from typing import Dict

from ..guild import Guild
from ..user import User
from .lootbox_types import LootboxTypes


@dataclass
class BaseData:
    total_attempts: int

    def to_dict(self) -> Dict:
        return {
            "totalAttempts": self.total_attempts
        }


@dataclass
class RolesData(BaseData):
   roles_attempts: int
   roles_got: int

   def to_dict(self) -> Dict:
        return {
            "totalAttempts": self.total_attempts,
            "rolesAttempts": self.roles_attempts,
            "rolesGot": self.roles_got
        }


@dataclass
class BackgroundsData(BaseData):
    backgrounds_attempts: int
    backgrounds_got: int

    def to_dict(self) -> Dict:
        return {
            "totalAttempts": self.total_attempts,
            "backgroundsAttempts": self.backgrounds_attempts,
            "backgroundsGot": self.backgrounds_got
        }


@dataclass
class LootboxUserData:
    guild_id: int
    guild: Guild
    user_id: int
    user: User
    lootbox_type: LootboxTypes
    data: BaseData

    def to_dict(self) -> Dict:
        return {
            "guildId": self.guild_id,
            "guild": self.guild,
            "userId": self.user_id,
            "user": self.user,
            "lootboxType": self.lootbox_type.value,
            "data": self.data.to_dict()
        }

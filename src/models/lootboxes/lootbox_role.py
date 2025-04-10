from dataclasses import dataclass
from typing import Dict, Optional

from ..guild import Guild
from .lootbox_types import LootboxTypes


@dataclass
class LootboxRole:
    guild_id: int
    guild: Optional[Guild]
    lootbox_type: LootboxTypes
    guild_role_id: int
    exclusive: bool
    got_by_user: Optional[bool]

    def to_dict(self) -> Dict:
        return {
            "guildId": self.guild_id,
            "guild": self.guild,
            "lootboxType": self.lootbox_type,
            "exclusive": self.exclusive,
            "guildRoleId": self.guild_role_id
        }
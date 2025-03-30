from dataclasses import dataclass
from typing import Optional
from disnake import Role as dRole

from .item import Item
from .items_config import ItemsConfig
from src.utils._extra import get_discord_role_by_id


@dataclass
class Role(Item):
    role_id: int
    guild_role_id: int

    @property
    def description(self) -> str:
        return ItemsConfig.get_formatted_desc(
            self.name, role_id=self.guild_role_id)
    
    @property
    def discord_role(self) -> Optional[dRole]:
        return get_discord_role_by_id(
            self.guild_id, self.guild_role_id)
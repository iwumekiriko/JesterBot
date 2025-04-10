from dataclasses import dataclass
from typing import Dict, Optional

from disnake import Role

from src.models.inventory_items.role import Role as IRole

from .shop_item import ShopItem
from src.utils._extra import get_discord_role_by_id


@dataclass
class ShopRole(ShopItem):
    guild_role_id: int
    exclusive: bool
    got_by_user: Optional[bool]
    price: int

    def to_dict(self) -> Dict:
        return {
            "guildId": self.guild_id,
            "guild": self.guild,
            "exclusive": self.exclusive,
            "guildRoleId": self.guild_role_id,
            "price": self.price
        }

    @property
    def discord_role(self) -> Optional[Role]:
        return get_discord_role_by_id(
            self.guild_id, self.guild_role_id)

    @property
    def inventory_item(self) -> IRole:
        return IRole(
            self.guild_id,
            self.guild,
            1, 0,
            self.guild_role_id
        )
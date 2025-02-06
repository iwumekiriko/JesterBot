from typing import Optional
import json

from .guild import Guild
from .user import User
from .inventory_items import Role, ExpBooster, LootboxKey


class Inventory:
    def __init__(
        self,
        inventory_id: int,
        guild_id: int,
        guild: Guild,
        user_id: int,
        user: User,
        roles: Optional[list[Role]] = None,
        exp_boosters: Optional[list[ExpBooster]] = None,
        lootbox_keys: Optional[list[LootboxKey]] = None
    ) -> None:
        self._inventory_id = inventory_id
        self._guild_id = guild_id
        self._guild = guild
        self._user_id = user_id
        self._user = user
        self._roles = roles
        self._exp_boosters = exp_boosters
        self._lootbox_keys = lootbox_keys

    @property
    def guild_id(self) -> int:
        return self._guild_id

    @property
    def guild(self) -> Guild:
        return self._guild

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def user(self) -> User:
        return self._user

    @property
    def roles(self) -> Optional[list[Role]]:
        return self._roles

    @property
    def exp_boosters(self) -> Optional[list[ExpBooster]]:
        return self._exp_boosters

    @property
    def lootbox_keys(self) -> Optional[list[LootboxKey]]:
        return self._lootbox_keys


    def __str__(self) -> str:
        inventory_to_str = (
            f"Guild Id: {self._guild_id}\n"
            f"User Id: {self._user_id}\n"
        )
        inventory_to_str += "\n"
        if self._roles:
            inventory_to_str += "Roles:\n\n"
            for role in self._roles:
                inventory_to_str += (
                    f"    Role Id: {role.member_role_id}\n"
                    f"    Type: {role.type.name}\n")
                if role.price:
                    inventory_to_str += (
                        f"    Price: {role.price}\n"
                    )
                if role.duration:
                    inventory_to_str += (
                        f"    Duration: {role.duration}\n"
                    )
                if role.description:
                    inventory_to_str += (
                        f"    Description: {role.description}\n"
                    )
                if role.lootbox_gif:
                    inventory_to_str += (
                        f"    Gif: {role.lootbox_gif.url}\n"
                    )
                if role.item_thumbnail:
                    inventory_to_str += (
                        f"    Thumbnail: {role.item_thumbnail.url}\n"
                    )
                if role.embed_color:
                    inventory_to_str += (
                        f"    Embed Color: {role.embed_color}\n"
                    )
                inventory_to_str += "    -----------------\n\n"
        if self._exp_boosters:
            inventory_to_str += "Exp Boosters:\n\n"
            for exp_booster in self._exp_boosters:
                inventory_to_str += f"    Amount: {exp_booster.count}\n"
                inventory_to_str += (
                    f"    Value: {exp_booster.value}\n"
                    f"    Duration: {exp_booster.duration}\n"
                )
                if exp_booster.description:
                    inventory_to_str += (
                        f"    Description: {exp_booster.description}\n"
                    )
                if exp_booster.lootbox_gif:
                    inventory_to_str += (
                        f"    Gif: {exp_booster.lootbox_gif.url}\n"
                    )
                if exp_booster.item_thumbnail:
                    inventory_to_str += (
                        f"    Thumbnail: {exp_booster.item_thumbnail.url}\n"
                    )
                inventory_to_str += "    -----------------\n\n"
        if self._lootbox_keys:
            inventory_to_str += "Lootbox Keys:\n\n"
            for key in self._lootbox_keys:
                inventory_to_str += f"    Amount: {key.count}\n"
                inventory_to_str += (
                    f"    Type: {key.type.name}\n"
                )
                if key.description:
                    inventory_to_str += (
                        f"    Description: {key.description}\n"
                    )
                if key.lootbox_gif:
                    inventory_to_str += (
                        f"    Gif: {key.lootbox_gif.url}\n"
                    )
                if key.item_thumbnail:
                    inventory_to_str += (
                        f"    Thumbnail: {key.item_thumbnail.url}\n"
                    )
                inventory_to_str += "    -----------------\n\n"
        return f"```{inventory_to_str}```"
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

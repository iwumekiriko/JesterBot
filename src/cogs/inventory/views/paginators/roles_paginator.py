from typing import Optional, List

import disnake

from src.localization import get_localizator

from src.utils.ui import BaseEmbed
from src.models.inventory_items import Role
from ..cards import RoleCard
from .inventory_items_paginator import InventoryItemsPaginator
from src.customisation import ROLES_SELECT_THUMBNAIL


_ = get_localizator("inventory-paginators")


class RolesPaginator(InventoryItemsPaginator[Role]):
    def __init__(
        self,
        items: Optional[List[Role]],
        guild_id: int,
        user_id: int,
        *,
        timeout: Optional[float] = 180,
    ) -> None:
        self._guild_id = guild_id
        self._user_id = user_id
        super().__init__(
            items = items or [],
            timeout = timeout,
            select_label_pattern="{index}. {item.discord_role.name}",
            card_type = RoleCard
        )

    def create_embed(self) -> disnake.Embed:
        return BaseEmbed(
            title = _("inventory-roles_paginator_embed_title"),
            description = _("inventory-roles_paginator_embed_desc")
        ).set_thumbnail(ROLES_SELECT_THUMBNAIL)

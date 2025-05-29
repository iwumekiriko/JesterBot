from typing import List, Optional

from src.logger import get_logger
from src.localization import get_localizator

from src.utils.ui import BaseEmbed
from src.models.inventory_items import LootboxKey
from ..cards import LootboxKeyCard
from ._inventory_items_paginator import InventoryItemsPaginator
from src.customisation import LOOTBOX_KEYS_SELECT_THUMBNAIL


logger = get_logger()
_ = get_localizator("inventory.paginators")


class LootboxKeysPaginator(InventoryItemsPaginator[LootboxKey]):
    def __init__(
        self,
        items: Optional[List[LootboxKey]],
        guild_id: int,
        user_id: int,
        *,
        timeout: Optional[float] = 180
    ) -> None:
        self._guild_id = guild_id
        self._user_id = user_id
        super().__init__(
            items = items or [],
            timeout = timeout,
            select_label_pattern="{index}. {item.type.translated}",
            card_type = LootboxKeyCard
        )

    def create_embed(self):
        return BaseEmbed(
            title = _("inventory-keys_paginator_embed_title"),
            description = _("inventory-keys_paginator_embed_desc")
        ).set_thumbnail(LOOTBOX_KEYS_SELECT_THUMBNAIL)

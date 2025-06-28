from typing import Optional

import disnake

from src.localization import get_localizator

from src.models.inventory_items import LootboxKey
from ._base_card import BaseCard


_ = get_localizator("inventory.cards")


class PackCard(BaseCard):
    def __init__(
        self,
        item: LootboxKey,
        *,
        timeout: Optional[float] = 180,
    ) -> None:
        super().__init__(item, timeout=timeout)

    def create_embed(self) -> disnake.Embed:
        return super().create_embed()
        
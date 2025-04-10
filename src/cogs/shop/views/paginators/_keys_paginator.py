from typing import Optional, List, Dict

import disnake

from ._shop_paginator import ShopPaginator
from src.models.shop import ShopKey
from ...embeds import ShopEmbed
from src.models.inventory_items import LootboxKey
from ..cards import KeysCard

from src.localization import get_localizator


_ = get_localizator("shop-paginators")


class KeysPaginator(ShopPaginator[ShopKey]):
    def __init__(
        self,
        guild: disnake.Guild,
        user: disnake.User,
        items: List[ShopKey],
        *,
        items_per_page: int = 10,
        timeout: Optional[float] = None
    ) -> None:
        self.items = items
        super().__init__(
            guild=guild,
            user=user,
            items=items,
            items_per_page=items_per_page,
            timeout=timeout
        )
        keys_select = KeysSelect()
        self.__updateable = [keys_select]
        self.add_item(keys_select)

        self._update_components()

    def create_embed(self) -> disnake.Embed:
        if not self.page_items:
            return ShopEmbed(title=_("shop-paginators-embed_empty"))

        from src.config import cfg
        lc = cfg.lootboxes_cfg(self._guild.id)
        ec = cfg.economy_cfg(self._guild.id)

        embed_desc = "\n".join([
            f"{i}. {key.lootbox_type.translated} — {lc.get_price(key.lootbox_type)} {ec.default_currency_icon}" 
            for i, key in enumerate(self.page_items, start=1)
        ])

        return ShopEmbed(
            title=_('shop-paginators-keys_embed_title'),
            description=embed_desc
        )
    
    def _update_components(self) -> None:
        for component in self.__updateable:
            component.update()


class KeysSelect(disnake.ui.Select):
    view: KeysPaginator

    def __init__(self) -> None:
        super().__init__()

    def update(self) -> None:
        if not self.view.page_items:
            self.options = [disnake.SelectOption(label="disabled")]
            self.disabled = True
            return

        self.options = [disnake.SelectOption(
            label=f"{index}. {key.lootbox_type.translated}", value=str(index) # type: ignore
        ) for index, key in enumerate(self.view.page_items, start=1)]

    async def callback(
        self,
        interaction: disnake.MessageInteraction
    ) -> None:
        await interaction.response.defer(with_message=False)

        from src.config import cfg

        lc = cfg.lootboxes_cfg(self.view._guild.id)

        key = self.view.page_items[int(self.values[0]) - 1]
        view = KeysCard(key, int(lc.get_price(key.lootbox_type)))
        await self.view.start_next(view)

from typing import Optional, List, Dict

import disnake

from ._shop_paginator import ShopPaginator
from src.models.shop import ShopPack
from ...embeds import ShopEmbed
from ..cards import PacksCard

from src.localization import get_localizator


_ = get_localizator("shop.paginators")


class PacksPaginator(ShopPaginator[ShopPack]):
    def __init__(
        self,
        guild: disnake.Guild,
        user: disnake.User,
        items: List[ShopPack],
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
        packs_select = PacksSelect()
        self.__updateable = [packs_select]
        self.add_item(packs_select)

        self._update_components()

    def create_embed(self) -> disnake.Embed:
        if not self.page_items:
            return ShopEmbed(title=_("shop-paginators-embed_empty"))

        from src.config import cfg
        pc = cfg.packs_cfg(self._guild.id)
        ec = cfg.economy_cfg(self._guild.id)

        embed_desc = "\n".join([
            f"{i}. {_('shop-paginators-pack_type', name=pack.name)} — {pc.packs_price} {ec.default_currency_icon}" 
            for i, pack in enumerate(self.page_items, start=1)
        ])

        return ShopEmbed(
            title=_('shop-paginators-packs_embed_title'),
            description=embed_desc
        )
    
    def _update_components(self) -> None:
        for component in self.__updateable:
            component.update()


class PacksSelect(disnake.ui.Select):
    view: PacksPaginator

    def __init__(self) -> None:
        super().__init__()

    def update(self) -> None:
        if not self.view.page_items:
            self.options = [disnake.SelectOption(label="disabled")]
            self.disabled = True
            return

        self.options = [disnake.SelectOption(
            label=f"{index}. {_('shop-paginators-pack_type', name=pack.name)}", value=str(index)
        ) for index, pack in enumerate(self.view.page_items, start=1)]

    async def callback(
        self,
        interaction: disnake.MessageInteraction
    ) -> None:
        await interaction.response.defer(with_message=False)

        from src.config import cfg

        pc = cfg.packs_cfg(self.view._guild.id)

        pack = self.view.page_items[int(self.values[0]) - 1]
        view = PacksCard(pack, int(pc.packs_price or 2000))
        await self.view.start_next(view)

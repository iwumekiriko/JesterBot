from typing import Optional, List, Dict

import disnake

from ._shop_paginator import ShopPaginator
from src.models.shop import ShopRole
from ..._api_interaction import get_user_shop_roles
from ...embeds import ShopEmbed
from src.models.inventory_items import Role
from ..cards import RolesCard

from src.localization import get_localizator


_ = get_localizator("shop.paginators")


class RolesPaginator(ShopPaginator[ShopRole]):
    def __init__(
        self,
        guild: disnake.Guild,
        user: disnake.User,
        items: List[ShopRole],
        *,
        items_per_page: int = 10,
        timeout: Optional[float] = None
    ) -> None:
        self.items: List[ShopRole] = items
        super().__init__(
            guild=guild,
            user=user,
            items=items,
            items_per_page=items_per_page,
            timeout=timeout
        )
        roles_select = RolesSelect()
        self.__updateable = [roles_select]
        self.add_item(roles_select)

        self._update_components()

    def create_embed(self) -> disnake.Embed:
        if not self.page_items:
            return ShopEmbed(title=_("shop-paginators-embed_empty"))

        from src.config import cfg
        ec = cfg.economy_cfg(self._guild.id)

        embed_desc = "\n".join([
            f"{index}. ~~<@&{role.guild_role_id}> — {role.price} {ec.default_currency_icon}~~ ({_('shop-paginators-roles-got_by_user')})"
            if role.got_by_user else f"{index}. <@&{role.guild_role_id}> — {role.price} {ec.default_currency_icon}"
            for index, role in enumerate(self.page_items, start=1)
        ])
        return ShopEmbed(
            title=_('shop-paginators-roles_embed_title'),
            description=embed_desc
        )
    
    def _update_components(self) -> None:
        for component in self.__updateable:
            component.update()


class RolesSelect(disnake.ui.Select):
    view: RolesPaginator

    def __init__(self) -> None:
        super().__init__()

    def update(self) -> None:
        if not self.view.page_items:
            self.options = [disnake.SelectOption(label="disabled")]
            self.disabled = True
            return

        self.options = [disnake.SelectOption(
            label=f"{index}. {role.discord_role.name}", value=str(index) # type: ignore
        ) for index, role in enumerate(self.view.page_items, start=1)]

    async def callback(
        self,
        interaction: disnake.MessageInteraction
    ) -> None:
        await interaction.response.defer(with_message=False)

        role = self.view.page_items[int(self.values[0]) - 1]
        view = RolesCard(role, role.price)
        await self.view.start_next(view)




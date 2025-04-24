from typing import Dict, Optional, Tuple, Callable

import disnake

from src.localization import get_localizator
from src.utils.ui import BaseView
from ..embeds import ShopEmbed
from .paginators import ShopPaginator, RolesPaginator, KeysPaginator
from .._api_interaction import get_shop_keys, get_user_shop_roles
from src.customisation import (
    SHOP_EMBED_THUMBNAIL,
    SHOP_KEEPER_NAME,
    GUILD_CURRENCY_NAME,
    GUILD_CURRENCY_SHORT_NAME
)


_ = get_localizator("shop")


class ShopCreationView(BaseView):
    def __init__(
        self,
        *,
        timeout: Optional[float] = None
    ) -> None:
        super().__init__(timeout=timeout)
        self.shop_categories: Dict[Tuple[str, str], Tuple[type[ShopPaginator], Callable]] = {
            (_("shop-roles_category"), "♣️"): (RolesPaginator, get_user_shop_roles),
            (_("shop-keys_category"), "🎫"): (KeysPaginator, get_shop_keys)
        }
        self.add_item(CategoriesSelect(self.shop_categories))

    def create_embed(self) -> disnake.Embed:
        return ShopEmbed(description = _('shop-embed_desc',
                        shop_keeper_name=SHOP_KEEPER_NAME,
                        guild_currency_short_name=GUILD_CURRENCY_SHORT_NAME,
                        guild_currency_name=GUILD_CURRENCY_NAME))


class CategoriesSelect(disnake.ui.Select):
    view: ShopCreationView

    def __init__(self, shop_categories: Dict) -> None:
        super().__init__(
            custom_id="shop-items-select-menu",
            options = [disnake.SelectOption(
                label=name, emoji=emoji
            ) for name, emoji in shop_categories]
        )

    async def callback(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ) -> None:
        name = self.values[0]
        view, func = next(
            (value for key, value in 
             self.view.shop_categories.items() if key[0] == name))

        guild: disnake.Guild = interaction.guild # type: ignore
        user: disnake.User = interaction.user # type: ignore

        items = await func(
            guild_id = guild.id, 
            user_id = user.id
        )
        await (view(guild, user, items)
            .start(interaction, {
                "items": items,
                "guild": interaction.guild,
                "user": interaction.user
        }))

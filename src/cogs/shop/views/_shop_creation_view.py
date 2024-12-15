from typing import Callable, Optional
import disnake

from src.utils._embeds import BaseEmbed
from .._role_purchase import (
    shop_select
)

from src.localization import get_localizator


_ = get_localizator("shop")


class ShopCreationView(disnake.ui.View):
    def __init__(
        self
    ) -> None:
        super().__init__(timeout=None)
        self.shop_options: dict[
            tuple[str, Optional[str]],
            Callable
        ] = {
            (_("role_shop"), "<:Misaka_What:1309256739245527160>"): shop_select
        }
        
        self.add_item(OpenShopSelect(self.shop_options))

    def create_embed(self) -> disnake.Embed:
        return BaseEmbed(
            title = _("welcome_shop_window_title"),
            description = _("welcome_shop_window_description")
        )

class OpenShopSelect(disnake.ui.Select):
    view: ShopCreationView

    def __init__(self, shop_options: dict) -> None:
        super().__init__(
            custom_id="open-shop-menu",
            options=[disnake.SelectOption(
                label=name, emoji=emoji)
                for name, emoji in shop_options])
   

    async def callback(
        self,
        interaction: disnake.MessageCommandInteraction
    ) -> None:
        name = self.values[0]
        await next((value for key, value in self.view.shop_options.items()
              if key[0] == name), shop_select)(interaction)
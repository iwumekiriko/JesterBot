from typing import Generic, List, Optional, TypeVar

import disnake

from src.utils.ui import Paginator, State
from src.models.shop import ShopItem

from src.localization import get_localizator


U = TypeVar("U", bound=ShopItem)
_ = get_localizator("shop-paginators")


class ShopPaginator(Paginator[U], Generic[U]):
    def __init__(
        self,
        guild: disnake.Guild,
        user: disnake.User,
        items: List[U],
        *,
        items_per_page: int = 10,
        timeout: Optional[float] = 300
    ) -> None:
        super().__init__(
            items=items,
            items_per_page=items_per_page,
            timeout=timeout
        )
        self._guild = guild
        self._user = user
        self.__updateable = []

    def create_embed(self) -> disnake.Embed:
        raise NotImplementedError
    
    async def _response(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ) -> None:
        await interaction.response.send_message(
            embed=self.create_embed(),
            view=self,
            ephemeral=True
        )

    def to_state(
        self, kwargs: Optional[dict] = None
    ) -> State:
        return State(
            view = self,
            embed = self.create_embed(),
            kwargs = kwargs
        )
    
    async def page_button_callback(
        self,
        interaction: disnake.MessageInteraction 
                    | disnake.ModalInteraction
    ) -> None:
        self._update_components()
        await interaction.response.edit_message(
            embed=self.create_embed(),
            view=self
        )

    def _update_components(self) -> None:
        for component in self.__updateable:
            component.update()

from typing import Optional

import disnake

from src.localization import get_localizator

from src.models.inventory import Inventory
from src.utils.ui import BaseView, BaseEmbed, State
from .paginators import RolesPaginator, BoostersPaginator, LootboxKeysPaginator
from src.customisation import CATEGORIES_SELECT_THUMBNAIL


_ = get_localizator("inventory-categories")


class InventoryCategoriesView(BaseView):
    def __init__(
        self,
        inventory: Inventory,
        *,
        timeout: Optional[float] = 300
    ) -> None:
        super().__init__(timeout = timeout)
        self.inventory = inventory
        self.categories = {
            _("inventory-roles_category"):
                (RolesPaginator, self.inventory.roles),
            _("inventory-exp_boosters_category"):
                (BoostersPaginator, self.inventory.exp_boosters),
            _("inventory-lootbox_keys_category"):
                (LootboxKeysPaginator, self.inventory.lootbox_keys),
        }
        self.add_item(CategoriesSelect(self.categories))

    def create_embed(self) -> disnake.Embed:
        return BaseEmbed(
            title = _("inventory-select_view_embed_title"),
            description = _("inventory-select_view_embed_desc")
        ).set_thumbnail(CATEGORIES_SELECT_THUMBNAIL)

    def to_state(
        self, kwargs: Optional[dict] = None
    ) -> State:
        return State(
            view = self,
            embed = self.create_embed(),
            kwargs = kwargs
        )

    async def _response(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ) -> None:
        await interaction.response.send_message(
            embed=self.create_embed(),
            view=self,
            ephemeral=True
        )


class CategoriesSelect(disnake.ui.Select):
    view: InventoryCategoriesView

    def __init__(self, categories: dict) -> None:
        super().__init__(
            options = [disnake.SelectOption(
                            label = name
                        ) for name in categories])

    async def callback(
        self,
        interaction: disnake.MessageInteraction
    ) -> None:
        view = self.view

        name = self.values[0]
        next_view, items = view.categories[name]

        await interaction.response.defer(with_message=False)
        n_v = next_view(
            items=items,
            guild_id=view.inventory.guild_id,
            user_id=view.inventory.user_id
        )
        await n_v.__ainit__()

        await view.start_next(
            n_v,
            {
                "items": items,
                "guild_id": view.inventory.guild_id,
                "user_id": view.inventory.user_id
            }
        )

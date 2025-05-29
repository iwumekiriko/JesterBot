import uuid
from typing import Optional

import disnake

from src.utils.ui import Paginator, BaseEmbed
from src.models.inventory_items import Item
from src.utils._cards import item_card
from src.customisation import PRIZES_PAGINATOR_THUMBNAIL

from src.localization import get_localizator


_ = get_localizator("lootboxes.common")


class LootboxesPrizesPaginator(Paginator[Item]):
    def __init__(
        self,
        items: Optional[list[Item]] = None,
        *,
        timeout: float | None = 600
    ) -> None:
        super().__init__(
            items=items or [],
            items_per_page=5,
            timeout=timeout
        )
        self.uuid = uuid.uuid4()
        self.current_item: Optional[Item] = self.first_item

        prizes_select = LootboxesPrizesSelect()
        self._updateable = [prizes_select]

        self.add_item(prizes_select)
        self._update_components()

    async def create_embed(self) -> disnake.Embed:
        if not (_c := self.current_item):
            return BaseEmbed(
                title=_("lootboxes-paginator_embed_title"),
                description=_("lootboxes-paginator_embed_desc")
            ).set_thumbnail(PRIZES_PAGINATOR_THUMBNAIL)
        return item_card(_c)

    async def _response(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ) -> None:
        await interaction.response.send_message(
            embed=await self.create_embed(),
            view=self
        )

    async def page_button_callback(
        self,
        interaction: disnake.MessageInteraction
                     | disnake.ModalInteraction
    ) -> None:
        self.current_item = self.first_item
        self._update_components()

        await interaction.response.edit_message(
            embed=await self.create_embed(),
            view=self
        )

    def update(self) -> None:
        super().update()
        if hasattr(self, '_updateable'):
            self._update_components()
            self.current_item = (self.current_item or
                                 self.first_item)

    def _update_components(self) -> None:
        for _i in self._updateable:
            _i.update()

    async def update_view(
        self,
        interaction: disnake.MessageInteraction
    ) -> None:
        self._update_components()
        await interaction.response.edit_message(
            embed =await self.create_embed(),
            view=self
        )


class LootboxesPrizesSelect(disnake.ui.Select):
    view: LootboxesPrizesPaginator

    def __init__(self) -> None:
        super().__init__()

    def update(self) -> None:
        if not self.view.page_items:
            self._set_disabled_state()
            return

        self._set_working_state()

    def _set_disabled_state(self) -> None:
        self.disabled = True
        self.placeholder = _("lootboxes-paginator_no_items_placeholder")
        self.options = [disnake.SelectOption(label="_")]

    def _set_working_state(self) -> None:
        self.disabled = False
        self.placeholder = _("lootboxes-paginator_items_placeholder")
        self.options = [
            disnake.SelectOption(
                label=f"{index}. {item.translated_name}",
                value=str(index - 1)
            ) for index, item 
            in enumerate(self.view.page_items, 1)]

    async def callback(
        self,
        interaction: disnake.MessageInteraction
    ) -> None:
        view = self.view
        index = int(self.values[0])
        view.current_item = view.page_items[index]
        await view.update_view(interaction)
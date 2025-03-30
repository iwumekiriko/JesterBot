from typing import Callable, Dict, Generic, List, Optional, Tuple, TypeVar
from abc import abstractmethod

import disnake

from src.logger import get_logger
from src.localization import get_localizator

from src.utils.ui import Paginator, State
from src.models.inventory_items import Item
from ..cards import BaseCard
from src.utils._time import hms_time_string


logger = get_logger()
_ = get_localizator("inventory-paginators")
U = TypeVar("U", bound = Item)


class InventoryItemsPaginator(Paginator[U], Generic[U]):
    def __init__(
        self,
        items: Optional[List[U]],
        *,
        timeout: Optional[float] = 180,
        select_label_pattern: str = "{index}.",
        card_type: type[BaseCard],
    ) -> None:
        self.card_type = card_type
        self.__updateable = []
        super().__init__(
            items = items or [],
            items_per_page = 5,
            timeout = timeout
        )
        items_select = InventoryItemsSelect(select_label_pattern)
        self.__updateable.append(items_select)
        self.add_item(items_select)

        self.add_back_button(row=2)
        self._update_components()

    @abstractmethod
    def create_embed(self):
        pass

    def _update_components(self) -> None:
        for component in self.__updateable:
            component.update()

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


class InventoryItemsSelect(disnake.ui.Select):
    view: InventoryItemsPaginator

    def __init__(self, label_pattern: str) -> None:
        super().__init__()
        self._label_pattern = label_pattern

    def update(self) -> None:
        if not self.view.page_items:
            self.options = [
                disnake.SelectOption(label="disabled")
            ]
            self.disabled = True
            return

        self.options = ([
            disnake.SelectOption(
                label = self._label_pattern.format(index=index, item=item),
                value = str(index - 1)
            ) for index, item 
            in enumerate(self.view.page_items, start=1)
        ])

    async def callback(
        self,
        interaction: disnake.MessageInteraction
    ) -> None:
        item = self.view.page_items[int(self.values[0])]
        await interaction.response.defer(with_message=False)
        await self.view.start_next(self.view.card_type(item), {"item": item})

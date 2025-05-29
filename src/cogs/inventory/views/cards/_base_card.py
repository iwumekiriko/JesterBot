from typing import Optional

from disnake import Embed

from src.localization import get_localizator

from src.utils.ui import BaseView
from src.utils._cards import item_card
from src.models.inventory_items import Item, ExpBooster
from src.utils.ui import State


_ = get_localizator("inventory.cards")


class BaseCard(BaseView):
    def __init__(
        self,
        item: Item,
        *,
        timeout: Optional[float] = 180
    ) -> None:
        self.item = item
        super().__init__(timeout=timeout)
        self.add_back_button()

    def create_embed(self) -> Embed:
        embed = item_card(self.item)

        return embed

    def to_state(
        self,
        kwargs: Optional[dict] = None
    ) -> State:
        return State(
            view = self,
            embed = self.create_embed(),
            kwargs = kwargs
        )

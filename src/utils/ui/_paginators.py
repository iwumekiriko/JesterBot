import disnake

from math import ceil
from typing import Optional, TypeVar, Generic, List

from src.utils.ui._views import BaseView
from ._modals import BaseModal, ModalTextInput
from src.localization import get_localizator


_ = get_localizator("ui")
T = TypeVar('T')


class Paginator(Generic[T], BaseView):
    def __init__(
        self,
        items: List[T],
        *,
        items_per_page: int = 1,
        timeout: Optional[float] = 180,
    ) -> None:
        super().__init__(timeout=timeout)

        self._all = items
        self._page_items: List[T] = []
        self._items_per_page = items_per_page
        self._page = 1
        self._max_page = self._count_max_page()

        self._page_buttons = []
        self._add_page_button(FirstPageButton())
        self._add_page_button(PreviousPageButton())
        self._add_page_button(CurrentPageButton())
        self._add_page_button(NextPageButton())
        self._add_page_button(LastPageButton())
        self.update()

    @property
    def page(self) -> int:
        return self._page

    @page.setter
    def page(self, page) -> None:
        self._page = self._adjust_page(page)
        self.update()

    @property
    def max_page(self) -> Optional[int]:
        return self._max_page

    @max_page.setter
    def max_page(self, max_page) -> None:
        self._max_page = self._adjust_page(max_page)
        self.update()

    @property
    def page_items(self) -> list[T]:
        return self._page_items

    @property
    def first_item(self) -> Optional[T]:
        if not self._page_items:
            return None

        return self._page_items[0]

    def update(self) -> None:
        page = self._page
        count = self._items_per_page

        self._page_items = self._all[(page-1)*count:page*count]
        self._update_page_buttons()

    def add(self, items: list[T]) -> None:
        self._all.extend(items)
        if self._max_page:
            self._max_page = self._count_max_page()
        self.update()

    def _count_max_page(self) -> int:
        return ceil(len(self._all) / self._items_per_page) or 1

    def _adjust_page(self, page: int) -> int:
        if self._max_page:
            page = min(page, self._max_page)
        page = max(1, page)
        return page

    def _update_page_buttons(self) -> None:
        for _button in self._page_buttons:
            _button.update()

    def _add_page_button(self, button: disnake.ui.Button) -> None:
        self.add_item(button)
        self._page_buttons.append(button)

    async def page_button_callback(
        self,
        interaction: disnake.MessageInteraction 
                    | disnake.ModalInteraction
    ) -> None:
        await interaction.response.edit_message(view=self)


class FirstPageButton(disnake.ui.Button):
    view: Paginator

    def __init__(self) -> None:
        super().__init__(
            emoji="⏮️",
            style=disnake.ButtonStyle.blurple
        )

    async def callback(
        self,
        interaction: disnake.MessageInteraction
    ) -> None:
        self.view.page = 1
        await self.view.page_button_callback(interaction)

    def update(self) -> None:
        self.disabled = self.view.page == 1


class PreviousPageButton(disnake.ui.Button):
    view: Paginator

    def __init__(self) -> None:
        super().__init__(
            emoji="◀️",
            style=disnake.ButtonStyle.blurple
        )

    async def callback(
        self,
        interaction: disnake.MessageInteraction
    ) -> None:
        self.view.page -= 1
        await self.view.page_button_callback(interaction)

    def update(self) -> None:
        self.disabled = self.view.page == 1


class CurrentPageButton(disnake.ui.Button):
    view: Paginator

    def __init__(self) -> None:
        super().__init__(
            style=disnake.ButtonStyle.blurple
        )

    async def callback(
        self,
        interaction: disnake.MessageCommandInteraction
    ) -> None:
        page_ = ModalTextInput(
            label=_("paginator_page_modal_field"),
            value=str(self.view.page),
            max_length=10
        )
        data = await BaseModal(
            title=_("paginator_page_modal"),
            components=[page_],
            interaction=interaction
        ).receive_data()
        if len(data) < 2:
            return

        inter: disnake.ModalInteraction = data[0]
        try:
            self.view.page = int(data[1])
        except ValueError:
            pass
        await self.view.page_button_callback(inter)

    def update(self) -> None:
        current = f"{str(self.view.page)}"
        if m_page:=self.view.max_page:
            current += f"/{m_page}"
        self.label = current


class NextPageButton(disnake.ui.Button):
    view: Paginator

    def __init__(self) -> None:
        super().__init__(
            emoji="▶️",
            style=disnake.ButtonStyle.blurple
        )

    async def callback(
        self,
        interaction: disnake.MessageInteraction
    ) -> None:
        self.view.page += 1
        await self.view.page_button_callback(interaction)

    def update(self) -> None:
        self.disabled = self.view.page == self.view.max_page


class LastPageButton(disnake.ui.Button):
    view: Paginator

    def __init__(self) -> None:
        super().__init__(
            emoji="⏭️",
            style=disnake.ButtonStyle.blurple
        )

    async def callback(
        self,
        interaction: disnake.MessageInteraction
    ) -> None:
        if self.view.max_page:
            self.view.page = self.view.max_page
        await self.view.page_button_callback(interaction)

    def update(self) -> None:
        self.disabled = self.view.page == self.view.max_page
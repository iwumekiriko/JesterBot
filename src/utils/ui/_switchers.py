from typing import Generic, TypeVar, Optional

import disnake

from ._views import BaseView


T = TypeVar('T', bound=BaseView)


class ViewSwitcher(disnake.ui.Select, Generic[T]):
    def __init__(self) -> None:
        super().__init__(row = 4)
        self._views: dict[str, T] = {}
        self._previous: Optional[T] = None

    def add_view(
        self,
        view: T,
        *,
        label: str
    ) -> None:
        view.add_item(self)
        super().add_option(label=label)
        self._views[label] = view

    async def start(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        start_index: int = 0
    ) -> None:
        view = list(self._views.values())[start_index]
        await view.start(interaction)

        message = view.message
        author = view.author
        for v in self._views.values():
            v.message = message
            v.author = author

    async def _response(
        self,
        view: T,
        interaction: disnake.MessageInteraction
    ) -> None:
        await interaction.response.edit_message(view=view)
    
    async def callback(
        self,
        interaction: disnake.MessageInteraction
    ) -> None:
        label = self.values[0]
        view = self._views[label]

        self._previous = view
        await self._response(view, interaction)

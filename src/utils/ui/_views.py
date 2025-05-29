from typing import List, Optional
from dataclasses import dataclass

import disnake

from src.localization import get_localizator
from src.utils._exceptions import CustomException
from src.utils.ui import ExceptionEmbed
from src.utils._exceptions import ModalTimeoutException


_ = get_localizator("general.ui")


@dataclass
class State:
    view: 'BaseView'
    content: Optional[str] = None
    embed: Optional[disnake.Embed] = None
    files: Optional[List[disnake.File]] = None
    kwargs: Optional[dict] = None


class ViewStates:
    def __init__(self, initial: State):
        self.__states: List[State] = [initial]

    def add_next(self, state: State) -> None:
        self.__states.append(state)

    @property
    def previous(self) -> State:
        if self.any_:
            self.__states.pop()
            return self.current
        return self.first

    @property
    def first(self) -> State:
        return self.__states[0]

    @property
    def current(self) -> State:
        return self.__states[-1]

    @property
    def any_(self) -> bool:
        return len(self.__states) > 1
    
    def __str__(self) -> str:
        return str(self.__states)


class BackButton(disnake.ui.Button):
    view: 'BaseView'

    def __init__(self, row: int) -> None:
        super().__init__(
            label=_("view_back_button"),
            style=disnake.ButtonStyle.gray,
            row=row
        )

    async def callback(
        self,
        interaction: disnake.MessageInteraction
    ) -> None:
        await interaction.response.defer()
        await self.view.to_previous()


class BaseView(disnake.ui.View):
    def __init__(
        self, *, timeout: Optional[float] = 180,
    ) -> None:
        super().__init__(timeout=timeout)
        self.author: disnake.Member | disnake.User
        self.message: disnake.Message
        self.states: ViewStates

    def to_state(
        self, kwargs: Optional[dict] = None
    ) -> State:
        return State(
            view = self,
            kwargs = kwargs
        )
    
    async def __ainit__(self) -> None:
        pass

    async def start(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        kwargs: Optional[dict] = None
    ) -> None:
        await self._response(interaction)
        self.message = await interaction.original_message()
        self.author = interaction.author
        self.states = ViewStates(self.to_state(kwargs))

    async def _response(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ) -> None:
        await interaction.response.send_message(
            view=self
        )

    async def start_next(
        self,
        view: 'BaseView',
        kwargs: Optional[dict] = None
    ) -> None:
        next_ = view
        next_.message = self.message
        next_.author = self.author
        next_state = next_.to_state(kwargs)

        self.states.add_next(next_state)
        next_.states = self.states

        await self.message.edit(
            view=next_state.view,
            content=next_state.content,
            embed=next_state.embed,
            files=next_state.files or []
        )
        self.stop()

    def add_back_button(self, row: int = 0) -> None:
        self.add_item(BackButton(row))

    async def to_previous(self) -> None:
        previous = self.states.previous

        v_type = type(previous.view)
        view = v_type(**(previous.kwargs) or {})
        await view.__ainit__()

        view.message = self.message
        view.author = self.author
        view.states = self.states

        await self.message.edit(
            view = view,
            embed = (view.create_embed() if hasattr(view, "create_embed") # type: ignore
                                         else previous.embed), 
            content = previous.content,
            files = previous.files or []
        )
        self.stop()

    async def interaction_check(
        self,
        interaction: disnake.MessageInteraction
    ) -> bool:
        if not hasattr(self, "author"):
            return True

        if not self.author.id == interaction.user.id:
            await interaction.response.send_message(
                _("not_an_interaction_author_err"),
                ephemeral=True
            )
            return False
        return True

    async def on_timeout(self) -> None:
        if not hasattr(self, "message"):
            return

        for item in self.children:
            item.disabled = True # type: ignore

        await self.message.edit(view=self)

    async def on_error(
        self,
        error: Exception,
        item: disnake.ui.Item,
        interaction: disnake.MessageInteraction
    ) -> None:
        if isinstance(error, ModalTimeoutException):
            return # neither we nor member should see this exception - redundant.
                   # in case we want to show some message - override timeout_handler() in modal class.

        if isinstance(error, CustomException):
            embed=ExceptionEmbed(error_msg=str(error))
            if interaction.response.is_done():
                await interaction.followup.send(
                    embed=embed,
                    ephemeral=True)
            else:
                await interaction.response.send_message(
                    embed=embed,
                    ephemeral=True)
        else:
            await super().on_error(error, item, interaction)

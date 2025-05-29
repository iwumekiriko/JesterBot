import asyncio
from typing import Optional, Union

import disnake

from src.localization import get_localizator

from src.utils.ui import BaseView, BaseEmbed
from .._api_interaction import become_duet


_ = get_localizator("duets.common")


class ProposalView(BaseView):
    def __init__(
        self,
        guild: disnake.Guild,
        proposer: Union[disnake.Member, disnake.User],
        duo: Union[disnake.Member, disnake.User],
        future: asyncio.Future,
        *,
        timeout: Optional[float] = 300
    ) -> None:
        self._guild = guild
        self._proposer = proposer
        self._duo = duo
        self._future = future
        super().__init__(timeout=timeout)

        accept_button = AcceptButton()
        deny_button = DenyButton()

        self.__updateable = [accept_button, deny_button]

        self.add_item(accept_button)
        self.add_item(deny_button)

    async def _response(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ) -> None:
        await interaction.response.send_message(
            content=self._duo.mention,
            embed=self.create_embed(),
            view=self
        )

    async def interaction_check(
        self,
        interaction: disnake.MessageInteraction
    ) -> bool:
        if interaction.user.id == (_d := self._duo.id):
            return True

        await interaction.response.send_message(
            content = _("duets-interaction_check_message", duo=_d),
            ephemeral = True
        )
        return False

    def create_embed(
        self,
        accepted: Optional[bool] = None
    ) -> disnake.Embed:
        match accepted:

            case True:
                return BaseEmbed(
                    title=_("duets-accepted_embed_title"),
                    description=_("duets-accepted_embed_desc",
                                  duo=self._duo.mention,
                                  proposer=self._proposer.mention)
                )

            case False:
                return BaseEmbed(
                    title=_("duets-denied_embed_title"),
                    description=_("duets-denied_embed_desc",
                                  duo=self._duo.mention,
                                  proposer=self._proposer.mention)
                )

            case _:
                return BaseEmbed(
                    title=_("duets-default_embed_title"),
                    description=_("duets-default_embed_desc",
                                  duo=self._duo.mention,
                                  proposer=self._proposer.mention)
                )

    async def handle_accept(
        self,
        interaction: disnake.MessageInteraction
    ) -> None:
        await become_duet(
            self._guild.id,
            self._proposer.id,
            self._duo.id
        )

        self.disable_buttons()
        await interaction.response.edit_message(
            embed=self.create_embed(accepted=True),
            view=self
        )

        if not self._future.done():
            self._future.set_result(True)

    async def handle_deny(
        self,
        interaction: disnake.MessageInteraction
    ) -> None:
        self.disable_buttons()
        await interaction.response.edit_message(
            embed=self.create_embed(accepted=False),
            view=self
        )

        if not self._future.done():
            self._future.set_result(False)

    def disable_buttons(self) -> None:
        for button in self.__updateable:
            button.disabled = True

    async def on_timeout(self) -> None:
        if not self._future.done():
            self._future.set_result(None)

        return await super().on_timeout()


class AcceptButton(disnake.ui.Button):
    view: ProposalView

    def __init__(self) -> None:
        super().__init__(
            label=_("duets-accept_button"),
            style=disnake.ButtonStyle.green
        )

    async def callback(
        self,
        interaction: disnake.MessageInteraction
    ) -> None:
        await self.view.handle_accept(interaction)


class DenyButton(disnake.ui.Button):
    view: ProposalView

    def __init__(self) -> None:
        super().__init__(
            label=_("duets-deny_button"),
            style=disnake.ButtonStyle.red
        )

    async def callback(
        self,
        interaction: disnake.MessageInteraction
    ) -> None:
        await self.view.handle_deny(interaction)
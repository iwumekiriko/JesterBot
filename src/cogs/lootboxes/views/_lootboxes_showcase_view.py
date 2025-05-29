import asyncio
from uuid import UUID
from typing import Dict, Optional, Union

import disnake

import disnake.ext
import disnake.ext.commands
from src.localization import get_localizator

from src.utils.ui._views import BaseView
from .._api_interaction import keys_count, manage_keys
from ..types import BaseLootbox, RolesLootbox, BackgroundsLootbox
from src.models.lootboxes import LootboxTypes
from ..types import BaseLootbox, RolesLootbox, BackgroundsLootbox


_ = get_localizator("lootboxes.common")


l_types: Dict[type[BaseLootbox], LootboxTypes] = {
    RolesLootbox: LootboxTypes.ROLES_LOOTBOX,
    BackgroundsLootbox: LootboxTypes.BACKGROUNDS_LOOTBOX
}


class LootboxesShowcaseView(BaseView):
    def __init__(
        self,
        guild: disnake.Guild,
        user: Union[disnake.User, disnake.Member],
        lootbox: type[BaseLootbox],
        uuid: UUID,
        *,
        timeout = 600
    ) -> None:
        super().__init__(timeout=timeout)
        self.uuid = uuid

        self._guild = guild
        self._user = user
        self._lootbox = lootbox
        self.__task: Optional[asyncio.Task] = None

        self.add_item(LootboxesOpenOneButton())
        self.add_item(LootboxesOpenAllButton())

    @property
    async def _keys_count(self) -> int:
        return await keys_count(
            self._guild.id, self._user.id,
            l_types[self._lootbox])

    async def create_embed(self) -> disnake.Embed:
        return await self._lootbox.create_embed(
            self._guild, self._user # type: ignore
        )

    async def _response(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ) -> None:
        await interaction.response.defer()
        embed = await self.create_embed()
        await interaction.followup.send(
            embed=embed, view=self)

    async def _process(
        self,
        interaction: disnake.MessageCommandInteraction,
        lootbox: type[BaseLootbox],
        count: int
    ) -> None:
        await manage_keys(self._guild.id, self._user.id,
                l_types[lootbox], -count)
        await lootbox(interaction, self.uuid).get_prize(count)

    async def _start_opening_task(
        self,
        interaction: disnake.MessageCommandInteraction,
        count: int
    ) -> None:
        if self.__task and not self.__task.done():
            return

        await self._on_task(on=True)
        self.__task = asyncio.create_task(
            self._process(interaction, self._lootbox, count))
        await self._wait_for_task()

    async def _wait_for_task(self) -> None:
        if not self.__task:
            return

        try: await self.__task
        except asyncio.CancelledError: pass
        finally:
            self.__task = None
            await self._on_task(on=False)

    async def _on_task(self, on: bool = True) -> None:
        for button in self.children:
            button.disabled = on # type: ignore
        await self.message.edit(view=self)

    async def _offer_to_buy(
        self,
        interaction: disnake.MessageCommandInteraction,
        lootbox: type[BaseLootbox]
    ) -> None:
        from ._lootboxes_buy_view import LootboxBuyView
        from .._lootbox_map import LootboxMap

        active = LootboxMap.is_active(
            lootbox, interaction.guild.id) # type: ignore
        
        if not active:
            raise disnake.ext.commands.BadArgument("no keys - not active")

        buy_view = LootboxBuyView(l_types[lootbox])
        await buy_view.start(interaction)

    async def handle_open(
        self, 
        interaction: disnake.MessageCommandInteraction,
        is_all: bool = False
    ) -> None:
        await interaction.response.defer()

        if not (_k := await self._keys_count) > 0:
            await self._offer_to_buy(interaction, self._lootbox)
            return
        
        if self.__task and not self.__task.done():
            return
        
        _c = _k if is_all else 1
        await self._start_opening_task(interaction, _c)

    async def on_timeout(self):
        if self.__task:
            self.__task.cancel()
        await super().on_timeout()


class LootboxesOpenOneButton(disnake.ui.Button):
    view: LootboxesShowcaseView

    def __init__(self) -> None:
        super().__init__(
            label=_("lootboxes-open_one_button"),
            style=disnake.ButtonStyle.green
        )

    async def callback(
        self,
        interaction: disnake.MessageCommandInteraction
    ) -> None:
        await self.view.handle_open(interaction, False)


class LootboxesOpenAllButton(disnake.ui.Button):
    def __init__(self) -> None:
        super().__init__(
            label=_("lootboxes-open_all_button"),
            style=disnake.ButtonStyle.blurple
        )

    async def callback(
        self,
        interaction: disnake.MessageCommandInteraction
    ) -> None:
        await self.view.handle_open(interaction, True)
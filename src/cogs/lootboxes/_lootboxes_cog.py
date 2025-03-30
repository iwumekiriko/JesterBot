import asyncio
from typing import Any, Dict, List
from uuid import UUID

import disnake
from disnake.ext import commands

from src.bot import JesterBot
from src.logger import get_logger
from src.localization import get_localizator

from ._api_interaction import handle_lootbox_role
from src.utils._permissions import for_admins
from ._lootbox_map import LootboxMap
from ._lootbox_roles_actions import LootboxRolesActions
from src.utils._events import CustomEvents
from src.models.inventory_items.item import Item
from src.utils.ui import ViewSwitcher
from .views import LootboxesShowcaseView, LootboxesPrizesPaginator
from src.utils._converters import dangerous_role_excluding


logger = get_logger()
_ = get_localizator("lootboxes")


LOOTBOXES_TIMEOUT = 600
REMOVE_TIMER = 1000


class LootboxesCog(commands.Cog):
    def __init__(self, bot: JesterBot):
        self.bot = bot
        self.__active: Dict[UUID, LootboxesPrizesPaginator] = {}

    async def _remove(self, uuid: UUID) -> None:
        await asyncio.sleep(REMOVE_TIMER)
        self.__active.pop(uuid, None)

    @commands.slash_command(description=_("lootboxes_desc"))
    async def lootboxes(
        self,
        interaction: disnake.GuildCommandInteraction,
        type = commands.Param(
            choices = {type.get_translated_name(): type for type in LootboxMap},
            description=_("lootboxes-type_param"))
    ) -> None:
        l_type = LootboxMap.get_type(type)
        guild = interaction.guild
        user = interaction.user

        _paginator = LootboxesPrizesPaginator(timeout=LOOTBOXES_TIMEOUT)
        _showcase = LootboxesShowcaseView(
            guild, user, l_type, _paginator.uuid, timeout=LOOTBOXES_TIMEOUT)

        self.__active[_paginator.uuid] = _paginator

        switcher = LootboxesViewSwitcher()
        switcher.add_view(_showcase, label=_("lootboxes-showcase_option"))
        switcher.add_view(_paginator, label=_("lootboxes-prizes_option"))
        await switcher.start(interaction)

        # view timeouts are 10 min, so 1000 sec must me enough for user 
        # to open everything he needs. And then we free the memory. 
        asyncio.create_task(self._remove(_paginator.uuid))

    @commands.Cog.listener(f'on_{CustomEvents.LOOTBOXES_ITEM_RECEIVED}')
    async def on_items_received(
        self,
        items: List[Item],
        uuid: UUID
    ) -> None:
        if _p := self.__active.get(uuid): _p.add(items)

    @commands.slash_command(**for_admins, description=_("lootboxes-role_desc"))
    async def lootboxes_role(
        self,
        interaction: disnake.GuildCommandInteraction,
        lootbox_type = commands.Param(
            choices = { type.get_translated_name(): type for type in LootboxMap.lootboxes_with_roles() },
            description=_("lootboxes-role-type_param")),
        action = commands.Param(
            choices = { action.get_translated_name(): action for action in LootboxRolesActions },
            description=_("lootboxes-role-action_param")),
        guild_role: disnake.Role = commands.Param(
            converter=dangerous_role_excluding, description=_("lootboxes-role-role_param"))
    ) -> None:
        l_type = LootboxMap.get_lootbox_type(lootbox_type)
        guild = interaction.guild

        await handle_lootbox_role(guild.id, l_type, guild_role.id, action)
        await interaction.response.send_message(_("lootboxes-success"), ephemeral=True)


class LootboxesViewSwitcher(ViewSwitcher):
    async def _response(
        self,
        view: Any,
        interaction: disnake.MessageInteraction
    ) -> None:
        await interaction.response.edit_message(
            embed=await view.create_embed(),
            view=view
        )
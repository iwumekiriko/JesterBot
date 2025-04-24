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
from src.utils._events import CustomEvents
from src.models.inventory_items.item import Item
from src.utils.ui import ViewSwitcher, SuccessEmbed
from .views import LootboxesShowcaseView, LootboxesPrizesPaginator
from src.utils._converters import dangerous_role_excluding
from src.utils.enums import Actions


logger = get_logger()
_ = get_localizator("lootboxes")


LOOTBOXES_TIMEOUT = 600
REMOVE_TIMER = 1000


def _active_lootboxes_autocomplete(
    inter: disnake.ApplicationCommandInteraction, arg
) -> Dict[str, str]:
    actives = LootboxMap.actives(inter.guild.id) # type: ignore
    return {lb.translated(): lb.value for lb in actives}


def _active_lootboxes_with_roles_autocomplete(
    inter: disnake.ApplicationCommandInteraction, arg
) -> Dict[str, str]:
    w_roles = LootboxMap.w_roles(inter.guild.id) # type: ignore
    return {lb.translated(): lb.value for lb in w_roles}


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
            autocomplete=_active_lootboxes_autocomplete,
            description=_("lootboxes-type_param"))
    ) -> None:
        l_type = LootboxMap.to_class(type)
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
    async def _lr(
        self,
        interaction: disnake.GuildCommandInteraction,
        lootbox_type = commands.Param(
            autocomplete=_active_lootboxes_with_roles_autocomplete,
            description=_("lootboxes-role-type_param")),
        action = commands.Param(
            choices = { action.get_translated_name(): action for action in Actions },
            description=_("lootboxes-role-action_param")),
        guild_role: disnake.Role = commands.Param(
            converter=dangerous_role_excluding, description=_("lootboxes-role-role_param")),
        exclusive: bool = commands.Param(description=_("lootboxes-role-exclusive_param"), default=False)
    ) -> None:
        await interaction.response.defer(ephemeral=True)

        l_type = LootboxMap.to_type(lootbox_type)
        guild = interaction.guild
        response = {
            Actions.ADD: _("lootboxes-role-add_success",
                                        role_id=guild_role.id, lootbox=l_type.translated),
            Actions.REMOVE: _("lootboxes-role-remove_success",
                                        role_id=guild_role.id, lootbox=l_type.translated)
        }
        await handle_lootbox_role(guild.id, l_type, guild_role.id, action, exclusive)
        await interaction.followup.send(
            embed=SuccessEmbed(success_msg=response[action])
        )


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
from typing import Dict, Optional, Tuple, Callable

import disnake

from src.localization import get_localizator
from src.utils.ui import BaseView
from ..embeds import QuestsEmbed
from ._quests_paginator import QuestsPaginator
from .._api_interaction import get_available_now_guild_quests, get_quest_board_img
from src.models.quests import QuestTypes
from src.customisation import QUESTS_KEEPER_NAME, QUESTS_KEEPER_AVATAR


_ = get_localizator("quests.views")


class QuestsBoardView(BaseView):
    def __init__(
        self,
        *,
        timeout: Optional[float] = None
    ) -> None:
        super().__init__(timeout=timeout)
        self.shop_categories: Dict[Tuple[str, str], QuestTypes] = {
            (_("quests-views-daily_category"), "🏕️"): QuestTypes.DAILY,
            (_("quests-views-weekly_category"), "🏜️"): QuestTypes.WEEKLY
        }
        self.add_item(CategoriesSelect(self.shop_categories))
        self._board_img_url = None

    def create_embed(self) -> disnake.Embed:
        return (QuestsEmbed(
            description = _('quest-views-board-embed-description',
                             board_keeper_name=QUESTS_KEEPER_NAME)
        ).set_image(self._board_img_url))

    async def set_board_img(self, guild_id: int) -> None:
        self._board_img_url = await get_quest_board_img(guild_id)


class CategoriesSelect(disnake.ui.Select):
    view: QuestsBoardView

    def __init__(self, shop_categories: Dict) -> None:
        super().__init__(
            custom_id="quests-board-select-menu",
            options = [disnake.SelectOption(
                label=name, emoji=emoji
            ) for name, emoji in shop_categories]
        )

    async def callback(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ) -> None:
        name = self.values[0]
        type = next(
             (value for key, value in 
             self.view.shop_categories.items() if key[0] == name))

        guild: disnake.Guild = interaction.guild # type: ignore
        user: disnake.User = interaction.user # type: ignore

        items = await get_available_now_guild_quests(
            guild_id = guild.id,
            user_id = user.id,
            type = type
        )
        await (QuestsPaginator(items)
            .start(interaction, {
                "items": items,
                "guild": interaction.guild,
                "user": interaction.user
        }))

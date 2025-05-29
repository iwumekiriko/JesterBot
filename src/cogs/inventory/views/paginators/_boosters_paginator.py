from typing import List, Optional

import disnake

from src.logger import get_logger
from src.localization import get_localizator

from src.utils._time import make_discord_timestamp
from src.utils.ui import BaseEmbed, SuccessEmbed
from src.models.inventory_items import ExpBooster
from ..cards import BoosterCard
from ._inventory_items_paginator import InventoryItemsPaginator
from ..._api_interaction import cancel_booster, get_active_booster
from src.customisation import EXP_BOOSTERS_SELECT_THUMBNAIL


logger = get_logger()
_ = get_localizator("inventory.paginators")


class BoostersPaginator(InventoryItemsPaginator[ExpBooster]):
    def __init__(
        self,
        items: Optional[List[ExpBooster]],
        guild_id: int,
        user_id: int,
        *,
        timeout: Optional[float] = 180,
    ) -> None:
        self.active_booster = None
        self._guild_id = guild_id
        self._user_id = user_id
        super().__init__(
            items = items or [],
            timeout = timeout,
            select_label_pattern = ("{index}. x{item.value} - "
                                    "{item.hms_duration}"),
            card_type = BoosterCard,
        )
        self.add_item(CancelBoosterButton())

    async def __ainit__(self) -> None:
        self.active_booster = await get_active_booster(
            self._guild_id, self._user_id)

    def create_embed(self):
        embed = BaseEmbed(
            title = _("inventory-boosters_paginator_embed_title"),
            description = _("inventory-boosters_paginator_embed_desc")
        ).set_thumbnail(EXP_BOOSTERS_SELECT_THUMBNAIL)
        if self.active_booster and self.active_booster.activated_at:
            embed.add_field(
                name="",
                value = _("inventory-boosters_paginator_embed_active_booster_desc",
                          value=self.active_booster.value,
                          timestamp=make_discord_timestamp(
                              self.active_booster.activated_at + 
                              self.active_booster.duration # type: ignore
                          )),
                inline=True
            )
        return embed

    async def update_view(self) -> None:
        await self.message.edit(
            embed=self.create_embed(),
            view=self
        )


class CancelBoosterButton(disnake.ui.Button):
    view: BoostersPaginator

    def __init__(self) -> None:
        super().__init__(
            label=_("inventory-boosters_paginator_cancel_button_label"),
            style=disnake.ButtonStyle.red
        )

    async def callback(
        self,
        interaction: disnake.MessageInteraction
    ) -> None:
        await interaction.response.defer(with_message=False)
        await cancel_booster(
            interaction.guild.id, # type: ignore
            interaction.user.id
        )
        self.view.active_booster = None
        await interaction.followup.send(
            embed=SuccessEmbed(
                success_msg=_("inventory-boosters_paginator_cancel_button_response")
            ),
            ephemeral=True
        )
        await self.view.update_view()
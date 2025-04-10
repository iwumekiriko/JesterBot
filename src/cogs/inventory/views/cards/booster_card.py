from typing import Optional

import disnake

from src.localization import get_localizator

from src.models.inventory_items import ExpBooster
from src.utils.ui import SuccessEmbed
from .base_card import BaseCard
from ..._api_interaction import use_booster


_ = get_localizator("inventory-cards")


class BoosterCard(BaseCard):
    def __init__(
        self,
        item: ExpBooster,
        *,
        timeout: Optional[float] = 180
    ) -> None:
        self.booster = item
        super().__init__(item, timeout=timeout)

        self.add_item(UseButton())

    def create_embed(self) -> disnake.Embed:
        return super().create_embed()

    async def update_view(
        self, interaction: disnake.MessageInteraction
    ) -> None:
        await interaction.message.edit(
            embed=self.create_embed(),
            view=self
        )

class UseButton(disnake.ui.Button):
    view: BoosterCard

    def __init__(self) -> None:
        super().__init__(
            label=_("inventory-card_boosters_use_button_label"),
            style=disnake.ButtonStyle.green
        )

    async def callback(
        self,
        interaction: disnake.MessageInteraction
    ) -> None:
        await interaction.response.defer(with_message=False)
        booster = self.view.booster
        await use_booster(
            interaction.guild.id, # type: ignore
            interaction.user.id,
            booster.value,
            booster.duration # type: ignore
        )
        booster.quantity -= 1

        await self.view.update_view(interaction)
        await interaction.followup.send(
            embed=SuccessEmbed(
                success_msg=_("inventory-card_boosters_use_button_response")
            ),
            ephemeral=True
        )

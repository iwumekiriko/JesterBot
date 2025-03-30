from typing import Optional

import disnake

from src.localization import get_localizator

from src.models.inventory_items import LootboxKey
from .base_card import BaseCard
from src.utils._extra import make_formatted_slash_command


_ = get_localizator("inventory-cards")


class LootboxKeyCard(BaseCard):
    def __init__(
        self,
        item: LootboxKey,
        *,
        timeout: Optional[float] = 180,
    ) -> None:
        super().__init__(item, timeout=timeout)
        self.add_item(UseButton())

    def create_embed(self) -> disnake.Embed:
        return super().create_embed()


class UseButton(disnake.ui.Button):
    def __init__(self) -> None:
        super().__init__(
            label=_("inventory-card_keys_use_button_label"),
            style=disnake.ButtonStyle.green
        )

    async def callback(
        self, interaction: disnake.MessageInteraction
    ) -> None:
        await interaction.response.send_message(
            content=_("inventory-card_keys_use_button_response",
                command=(make_formatted_slash_command("lootboxes")
                        or "`command not found`")),
            ephemeral=True
        )
        
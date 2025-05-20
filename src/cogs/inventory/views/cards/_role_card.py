from typing import Optional

import disnake

from src.localization import get_localizator

from src.models.inventory_items import Role
from src.utils._extra import (
    add_role_with_id, remove_role_with_id)
from ._base_card import BaseCard


_ = get_localizator("inventory-cards")


class RoleCard(BaseCard):
    def __init__(
        self,
        item: Role,
        *,
        timeout: Optional[float] = 180
    ) -> None:
        super().__init__(item, timeout=timeout)
        self.add_item(AddRoleButton())
        self.add_item(RemoveRoleButton())


class AddRoleButton(disnake.ui.Button):
    view: RoleCard

    def __init__(self) -> None:
        super().__init__(
            label = _("inventory-card_roles_add_button_label"),
            style = disnake.ButtonStyle.green
        )

    async def callback(
        self,
        interaction: disnake.MessageInteraction
    ) -> None:
        guild: disnake.Guild = interaction.guild # type: ignore
        member: disnake.Member = interaction.user # type: ignore

        await interaction.response.defer(with_message=False)
        await add_role_with_id(
            guild, member,
            self.view.item.guild_role_id # type: ignore
        )


class RemoveRoleButton(disnake.ui.Button):
    view: RoleCard

    def __init__(self) -> None:
        super().__init__(
            label = _("inventory-card_roles_remove_button_label"),
            style = disnake.ButtonStyle.red
        )

    async def callback(
        self,
        interaction: disnake.MessageInteraction
    ) -> None:
        guild: disnake.Guild = interaction.guild # type: ignore
        member: disnake.Member = interaction.user # type: ignore

        await interaction.response.defer(with_message=False)
        await remove_role_with_id(
            guild, member,
            self.view.item.guild_role_id # type: ignore
        )
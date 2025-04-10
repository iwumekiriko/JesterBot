from typing import Optional

import disnake

from ._base_card import BaseCard, BuyOneButton, TryButton
from src.models.shop import ShopRole
from src.models.inventory_items import Role
from src.utils._extra import add_role_with_id
from ..._api_interaction import get_shop_role_tries, try_shop_role
from src.utils.ui import SuccessEmbed
from src.utils._exceptions import AlreadyOwnsRoleException


MAX_ROLE_TRIES = 2


class RolesCard(BaseCard):
    def __init__(
        self,
        item: ShopRole,
        price: int,
        *,
        timeout: Optional[float] = 180
    ) -> None:
        super().__init__(
            item=item,
            price=price,
            timeout=timeout
        )

        buy_one_role_button = BuyOneRoleButton()
        try_role_button = TryRoleButton()
        self.__updateable = [
            buy_one_role_button,
            try_role_button
        ]

        self.add_item(buy_one_role_button)
        self.add_item(try_role_button)
        self._update_components()

    async def handle_buy(
        self,
        interaction: disnake.MessageInteraction,
    ) -> None:
        await interaction.response.defer(with_message=False)

        from src.cogs.lootboxes._api_interaction import add_item_to_inventory

        guild: disnake.Guild = interaction.guild # type: ignore
        user: disnake.Member = interaction.user # type: ignore
        role: ShopRole = self._item # type: ignore

        start_coins, left_coins = await self.charge_price(guild.id, user.id)

        try:
            await add_item_to_inventory(
                guild.id, user.id, Role,
                body={"GuildRoleId": role.guild_role_id}
            )
            await add_role_with_id(guild, user, role.guild_role_id)

            role.got_by_user = True
            self._update_components()
            await super().handle_buy(interaction, start_coins, left_coins)
        except AlreadyOwnsRoleException:
            await self.refund(guild.id, user.id, self._price)
            raise

    async def handle_try(
        self,
        interaction: disnake.MessageInteraction
    ) -> None:
        await interaction.response.defer(ephemeral=True)

        guild: disnake.Guild = interaction.guild # type: ignore
        user: disnake.Member = interaction.user # type: ignore
        role: Role = self._item # type: ignore

        await try_shop_role(guild.id, user.id, role.guild_role_id)
        await add_role_with_id(guild, user, role.guild_role_id)
        await super().handle_try(interaction)

    def _update_components(self) -> None:
        for component in self.__updateable:
            component.update()


class BuyOneRoleButton(BuyOneButton):
    view: RolesCard

    def update(self) -> None:
        item = self.view._item
        self.disabled = (bool(item.got_by_user) 
                        if isinstance(item, ShopRole) else False)


class TryRoleButton(TryButton):
    view: RolesCard

    def update(self) -> None:
        item = self.view._item
        self.disabled = (bool(item.got_by_user) 
                        if isinstance(item, ShopRole) else False)

    async def callback(
        self,
        interaction: disnake.MessageInteraction
    ) -> None:
        tries_data = await get_shop_role_tries(
            interaction.guild.id, # type: ignore
            interaction.user.id,
            self.view._item.guild_role_id # type: ignore
        )
        await super().callback(
            interaction,
            warning=("shop-cards-try_role_warning", {
                "guild_role_id": tries_data.guild_role_id,
                "left_tries": MAX_ROLE_TRIES - tries_data.tries_used
            })
        )
        if not interaction.response.is_done():
            await self.view.handle_try(interaction)
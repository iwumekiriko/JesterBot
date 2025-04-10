from typing import Optional

import disnake

from ._base_card import BaseCard, BuyOneButton, BuyManyButton
from src.models.shop import ShopKey
from src.utils.ui import SuccessEmbed


class KeysCard(BaseCard):
    def __init__(
        self,
        item: ShopKey,
        price: int,
        *,
        timeout: Optional[float] = 180
    ) -> None:
        super().__init__(
            item=item,
            price=price,
            timeout=timeout
        )

        self.add_item(BuyOneKeyButton())
        self.add_item(BuyManyKeysButton())

    async def handle_buy(
        self,
        interaction: disnake.MessageInteraction,
        count: int = 1
    ) -> None:
        await interaction.response.defer(ephemeral=True)

        from src.cogs.lootboxes._api_interaction import manage_keys

        guild: disnake.Guild = interaction.guild # type: ignore
        user: disnake.Member = interaction.user # type: ignore
        key: ShopKey = self._item # type: ignore

        start_coins, left_coins = await self.charge_price(guild.id, user.id, count)
        try:
            await manage_keys(guild.id, user.id, key.lootbox_type, count)
            await super().handle_buy(interaction, start_coins, left_coins)
        except:
            await self.refund(guild.id, user.id, self._price)
            raise


class BuyOneKeyButton(BuyOneButton):
    view: KeysCard


class BuyManyKeysButton(BuyManyButton):
    view: KeysCard
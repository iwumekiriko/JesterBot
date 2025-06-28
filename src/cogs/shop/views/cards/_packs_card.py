from typing import Optional

import disnake

from ._base_card import BaseCard, BuyOneButton, BuyManyButton
from src.models.shop import ShopPack
from src.utils.ui import SuccessEmbed


class PacksCard(BaseCard):
    def __init__(
        self,
        item: ShopPack,
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
        await interaction.response.defer(with_message=False, ephemeral=True)

        from src.cogs.lootboxes._api_interaction import update_packs

        guild: disnake.Guild = interaction.guild # type: ignore
        user: disnake.Member = interaction.user # type: ignore
        pack: ShopPack = self._item # type: ignore

        start_coins, left_coins = await self.charge_price(guild.id, user.id, count)
        try:
            await update_packs(guild.id, user.id, pack.id, count)
            await super().handle_buy(interaction, start_coins, left_coins)
        except:
            await self.refund(guild.id, user.id, self._price)
            raise


class BuyOneKeyButton(BuyOneButton):
    view: PacksCard


class BuyManyKeysButton(BuyManyButton):
    view: PacksCard
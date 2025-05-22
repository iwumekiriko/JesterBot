from typing import Optional, Tuple

import disnake

from src.models.shop import ShopItem, ShopRole
from src.utils.ui import BaseView, State, SuccessEmbed, WarningEmbed, ModalTextInput, BaseModal
from src.utils._cards import item_card

from src.localization import get_localizator


_ = get_localizator("shop-cards")


class BaseCard(BaseView):
    def __init__(
        self,
        item: ShopItem,
        price: int,
        *,
        timeout: Optional[float] = 180
    ) -> None:
        self._item = item
        self._price = price

        super().__init__(timeout=timeout)
        self.add_back_button()

    def create_embed(self) -> disnake.Embed:
        return (item_card(self._item.inventory_item, False)
            .add_field(
                name="",
                value=(f"{_('shop-cards-embed_price_field')}: ~~**{self._price}**~~ ({_('shop-cards-got_by_user')})" 
                       if isinstance(self._item, ShopRole) and self._item.got_by_user else
                       f"{_('shop-cards-embed_price_field')}: **{self._price}**")
            ))

    def to_state(
        self,
        kwargs: Optional[dict] = None
    ) -> State:
        return State(
            view = self,
            embed = self.create_embed(),
            kwargs = kwargs
        )

    async def handle_buy(
        self,
        interaction: disnake.MessageInteraction,
        start_coins: int,
        left_coins: int
    ) -> None:
        from src.config import cfg
        currency_icon = cfg.economy_cfg(interaction.guild.id).default_currency_icon # type: ignore

        await self.update_view()
        await interaction.followup.send(
            embed=SuccessEmbed(
                success_msg=_("shop-cards-buy_success", 
                    start_coins=start_coins,
                    left_coins=left_coins,
                    currency_icon=currency_icon
                )
            ),
            ephemeral=True
        )

    async def charge_price(
        self,
        guild_id: int,
        user_id: int,
        count: int = 1
    ) -> Tuple[int, int]:
        from src.cogs.economy._api_interaction import make_coins_transaction
        member_data = await make_coins_transaction(guild_id, user_id, abs(self._price * count))

        left_coins = member_data.coins
        start_coins = left_coins + self._price * count

        return (start_coins, left_coins)

    async def refund(
        self,
        guild_id: int,
        user_id: int,
        amount: int
    ) -> None:
        from src.cogs.economy._api_interaction import make_coins_transaction
        await make_coins_transaction(guild_id, user_id, -amount)

    async def handle_try(
        self,
        interaction: disnake.MessageInteraction
    ) -> None:
        await interaction.followup.send(
            embed=SuccessEmbed(
                success_msg=_("shop-cards-try_success"),
            ),
            ephemeral=True
        )

    async def update_view(self) -> None:
        await self.message.edit(
            view=self,
            embed=self.create_embed()
        )


class BuyOneButton(disnake.ui.Button):
    def __init__(self) -> None:
        super().__init__(
            label=_("shop-cards-buy_one_button_label"),
            style=disnake.ButtonStyle.green
        )

    async def callback(
        self,
        interaction: disnake.MessageInteraction
    ) -> None:
        await self.view.handle_buy(interaction)


class BuyManyButton(disnake.ui.Button):
    def __init__(self) -> None:
        super().__init__(
            label=_("shop-cards-buy_many_button_label"),
            style=disnake.ButtonStyle.blurple
        )

    async def callback(
        self,
        interaction: disnake.MessageInteraction
    ) -> None:
        count_in = ModalTextInput(
            label=_("shop-cards-buy_many_modal_count_input"),
            max_length=5,
            min_length=1
        )

        modal_data = await BaseModal(
            title=_("shop-cards-buy_many_modal_label"),
            components=[count_in],
            interaction=interaction, # type: ignore
            timeout=30
        ).receive_data()
        if len(modal_data) < 2:
            return

        inter: disnake.ModalInteraction = modal_data[0]
        try:
            count: int = abs(int(modal_data[1]))
            if count == 0:
                return

            await self.view.handle_buy(inter, count)
        except ValueError:
            pass


class TryButton(disnake.ui.Button):
    def __init__(self) -> None:
        super().__init__(
            label=_("shop-cards-try_button_label"),
            style=disnake.ButtonStyle.blurple
        )
        self.warned: bool = False

    async def callback(
        self,
        interaction: disnake.MessageInteraction,
        warning: Tuple[str, dict]
    ) -> None:
        warning_local, kwargs = warning
        if not self.warned:
            self.warned = True
            await interaction.response.send_message(
                embed=WarningEmbed(warning_msg=_(warning_local, **kwargs)),
                ephemeral=True
            )

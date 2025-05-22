import disnake

from src.utils.ui import BaseView, ModalTextInput, BaseModal, SuccessEmbed
from src.localization import get_localizator
from .._api_interaction import manage_keys
from src.cogs.economy._api_interaction import make_coins_transaction
from src.models.lootboxes import LootboxTypes


_ = get_localizator("lootboxes")


class LootboxBuyView(BaseView):
    def __init__(
        self,
        key_type: LootboxTypes,
        *,
        timeout: int = 60,
    ) -> None:
        super().__init__(timeout=timeout)
        self._key_type = key_type
        self.add_item(LootboxBuyOneButton())
        self.add_item(LootboxBuyManyButton())

    async def _response(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ) -> None:
        from src.config import cfg
        lc = cfg.lootboxes_cfg(interaction.guild.id) # type: ignore
        ec = cfg.economy_cfg(interaction.guild.id) # type: ignore
        price = lc.get_price(self._key_type)
        currency = ec.default_currency_icon

        await interaction.followup.send(
            embed=disnake.Embed(
                title=_("lootboxes-buy_embed_title"),
                description=_("lootboxes-buy_embed_desc",
                               price=price, currency=currency)
            ),
            view=self,
            ephemeral=True)

    async def buy_(
        self,
        guild_id: int, user_id: int,
        price: int, count: int
    ) -> int:
        if count > 1:
            price *= count

        member = await make_coins_transaction(guild_id, user_id, price)
        await manage_keys(guild_id, user_id, self._key_type, count)

        return member.coins

    async def _handle_button(
        self,
        interaction: disnake.MessageInteraction
                     | disnake.ModalInteraction,
        count: int = 1
    ) -> None:
        guild_id = interaction.guild.id # type: ignore
        user_id = interaction.user.id

        from src.config import cfg
        lc = cfg.lootboxes_cfg(guild_id)
        ec = cfg.economy_cfg(guild_id)
        price = int(lc.get_price(self._key_type))
        currency_icon = ec.default_currency_icon

        left_coins = await self.buy_(guild_id, user_id, price, count)
        await interaction.followup.send(
            embed=SuccessEmbed(
                success_msg=_("lootboxes-buy_success", 
                    start_coins=left_coins+price*count,
                    left_coins=left_coins,
                    currency_icon=currency_icon
                )
            ),
            ephemeral=True
        )

    async def on_timeout(self) -> None:
        self.stop()


class LootboxBuyOneButton(disnake.ui.Button):
    view: LootboxBuyView

    def __init__(self) -> None:
        super().__init__(
            label=_("lootboxes-buy_one_button"),
            style=disnake.ButtonStyle.gray
        )

    async def callback(
        self,
        interaction: disnake.MessageInteraction
    ) -> None:
        await interaction.response.defer(with_message=False)
        await self.view._handle_button(interaction)

class LootboxBuyManyButton(disnake.ui.Button):
    view: LootboxBuyView

    def __init__(self) -> None:
        super().__init__(
            label=_("lootboxes-buy_many_button"),
            style=disnake.ButtonStyle.blurple
        )

    async def callback(
        self,
        interaction: disnake.MessageCommandInteraction
    ) -> None:
        count_in = ModalTextInput(
            label=_("lootboxes-buy_modal_count_input"),
            max_length=5,
            min_length=1
        )

        modal_data = await BaseModal(
            title=_("lootboxes-buy_modal_label"),
            components=[count_in],
            interaction=interaction,
            timeout=30
        ).receive_data()
        if len(modal_data) < 2:
            return

        inter: disnake.ModalInteraction = modal_data[0]
        try:
            await interaction.response.defer(with_message=False)
            count: int = abs(int(modal_data[1]))
            await self.view._handle_button(inter, count)
        except ValueError:
            pass
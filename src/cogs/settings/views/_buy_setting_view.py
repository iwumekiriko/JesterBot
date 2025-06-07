from asyncio import Future
from typing import Optional

import disnake

from src.utils.ui import BaseView, BaseEmbed, SuccessEmbed
from src.models.settings import Setting
from src.utils.enums import Currency

from src.localization import get_localizator


_ = get_localizator("settings.views")


class BuySettingView(BaseView):
    def __init__(
        self,
        guild_id: int,
        user_id: int,
        future: Future,
        setting: Setting,
        timeout: Optional[float] = 180,
    ) -> None:
        super().__init__(timeout=timeout)
        self._user_id = user_id
        self._guild_id = guild_id
        self._future = future
        self._setting = setting

        self.add_item(BuyAcceptButton())
        self.add_item(BuyDenyButton())

    def create_embed(self) -> disnake.Embed:
        return BaseEmbed(
            title=_("buy_embed_title"),
            description=_("buy_embed_desc",
                        cost=self._setting.cost,
                        currency=Currency.CRYSTALS.get_icon(self._guild_id))
        )

    async def _response(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ) -> None:
        await interaction.response.send_message(
            embed=self.create_embed(),
            view=self,
            ephemeral=True
        )

    async def on_timeout(self) -> None:
        if not self._future.done():
            self._future.set_result(False)
        return await super().on_timeout()


class BuyAcceptButton(disnake.ui.Button):
    view: BuySettingView

    def __init__(self) -> None:
        super().__init__(
            label=_("buy_approve_button_label"),
            style=disnake.ButtonStyle.green 
        )

    async def callback(
        self,
        interaction: disnake.MessageInteraction
    ) -> None:
        from src.cogs.economy._api_interaction import make_transaction

        view = self.view
        await interaction.response.defer()
        member_data = await make_transaction(
            Currency.CRYSTALS,
            interaction.guild.id, # type: ignore
            interaction.user.id,
            view._setting.cost
        )

        left_crystals = member_data.crystals
        start_crystals = left_crystals + view._setting.cost

        await view.message.edit(
            embed=SuccessEmbed(
                success_msg=_("success_buy_message",
                              start_crystals=start_crystals,
                              left_crystals=left_crystals,
                              currency_icon=Currency.CRYSTALS.get_icon(view._guild_id))
            ), view=None)

        view.stop()
        await view.message.delete(delay=3)
        view._future.set_result(True)


class BuyDenyButton(disnake.ui.Button):
    view: BuySettingView

    def __init__(self) -> None:
        super().__init__(
            label=_("buy_deny_button_label"),
            style=disnake.ButtonStyle.red
        )

    async def callback(
        self,
        interaction: disnake.MessageInteraction
    ) -> None:
        view = self.view
        await interaction.response.defer()

        view.stop()
        await view.message.delete()
        view._future.set_result(False)

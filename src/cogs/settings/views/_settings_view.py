from typing import Optional
from asyncio import Future, CancelledError

import disnake

from src.utils.ui import BaseView
from src.models.settings import UserSettings, SettingTypes
from src.utils._cards import settings_card
from ._buy_setting_view import BuySettingView
from .._api_interaction import update_setting

from src.localization import get_localizator


_ = get_localizator("settings.views")


class SettingsView(BaseView):
    def __init__(
        self,
        settings: UserSettings,
        timeout: Optional[float] = 180
    ) -> None:
        self.u_settings = settings
        super().__init__(timeout=timeout)

        settings_select = SettingsSelect()

        self.__updateable = [settings_select]
        self.add_item(settings_select)

        self._update_components()

    def create_embed(self) -> disnake.Embed:
        return settings_card(self.u_settings)

    async def _response(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ) -> None:
        await interaction.response.send_message(
            embed=self.create_embed(),
            view=self,
            ephemeral=True
        )

    def _update_components(self) -> None:
        for component in self.__updateable:
            component.update()

    async def update_view(self) -> None:
        await self.message.edit(
            embed=self.create_embed(),
            view=self
        )


class SettingsSelect(disnake.ui.Select):
    view: SettingsView

    def __init__(self) -> None:
        super().__init__()

    def update(self) -> None:
        u_settings = self.view.u_settings

        self.options = [
            disnake.SelectOption(
                label = setting.type.translated,
                value = str(setting.type.value)
            )
            for setting in u_settings.settings
        ]

    async def callback(
        self,
        interaction: disnake.MessageInteraction
    ) -> None:
        type_value = int(self.values[0])
        setting = next(s for s in self.view.u_settings.settings
                        if s.type == SettingTypes(type_value))
        
        guild_id=interaction.guild.id # type: ignore
        user_id=interaction.user.id

        if not setting.bought:
            future = Future()
            view = BuySettingView(
                guild_id=guild_id, 
                user_id=user_id,
                future=future,
                setting=setting,
                timeout=60
            )
            await view.start(interaction) # type: ignore
            try:
                result = await future
            except CancelledError:
                result = False

            if result == True:
                setting.bought = True
                setting.state = not setting.state
                await update_setting(guild_id, user_id, setting)
        else:
            await interaction.response.defer()
            setting.state = not setting.state
            await update_setting(guild_id, user_id, setting)

        await self.view.update_view()

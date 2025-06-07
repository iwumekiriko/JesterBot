import disnake
from disnake.ext import commands

from src.bot import JesterBot
from src.logger import get_logger
from src.localization import get_localizator

from ._api_interaction import get_user_settings, update_guild_setting
from .views import SettingsView
from src.models.settings import SettingTypes
from src.utils.enums import Actions
from src.utils.ui import SuccessEmbed
from src.utils._permissions import for_admins


logger = get_logger()
_ = get_localizator("settings.common")


class SettingsCog(commands.Cog):
    def __init__(self, bot: JesterBot) -> None:
        self._bot = bot

    @commands.slash_command(description=_("settings_desc"))
    async def settings(
        self,
        interaction: disnake.GuildCommandInteraction
    ) -> None:
        settings = await get_user_settings(interaction.guild.id, interaction.user.id)
        view = SettingsView(settings, timeout=180)
        await view.start(interaction)

    @commands.slash_command(**for_admins, description=_("guild_setting_desc"))
    async def _gs(
        self,
        interaction: disnake.GuildCommandInteraction,
        action = commands.Param(
            choices = { action.get_translated_name(): action for action in Actions },
            description=_("action_param")),
        type = commands.Param(
            description=_("type_param"),
            choices={ type.translated: str(type.value) for type in SettingTypes }),
        cost: int = commands.Param(description=_("cost_param"), default=0)
    ) -> None:
        await interaction.response.defer(ephemeral=True)
        type = SettingTypes(int(type))
        await update_guild_setting(action, interaction.guild.id, type, cost)
        await interaction.followup.send(embed=SuccessEmbed(
            success_msg=_("success_update_setting_message", type=type.translated)))

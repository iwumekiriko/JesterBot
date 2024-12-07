import disnake
from disnake.ext import commands

from src.bot import JesterBot
from src.models.config import *
from src.utils._permissions import for_admins
from .views._config_view import ConfigView


class ConfigCog(commands.Cog):
    def __init__(self, bot: JesterBot) -> None:
        self.bot = bot

    @commands.slash_command(**for_admins)
    async def config(
        self,
        interaction: disnake.GuildCommandInteraction
    ) -> None:
        view = ConfigView(interaction.guild_id)
        await view.start(interaction)

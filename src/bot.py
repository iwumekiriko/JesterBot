import disnake
from disnake.ext import commands

from datetime import datetime
from src._cog_manager import CogManager
from src.logger import get_logger
from src.localization import get_localizator
from src.utils._exceptions import CustomException
from src.utils.ui import ExceptionEmbed
from src import settings


logger = get_logger()
_ = get_localizator()


class JesterBot(commands.Bot):
    def __init__(self) -> None:
        intents = disnake.Intents.all()
        command_sync_flags = commands.CommandSyncFlags.all()
        command_sync_flags.sync_commands_debug = settings.DEBUG

        super().__init__(
            intents=intents,
            command_sync_flags=command_sync_flags,
            command_prefix=["?", "::"]
        )
        self._load_cogs()
        self.__persistent_views_added = False

    async def on_connect(self) -> None:
        from src.config import cfg
        await cfg.load()

    async def on_ready(self) -> None:
        if not self.__persistent_views_added:
            from src.cogs.tickets.views._ticket_creation_view import TicketCreationView
            from src.cogs.tickets.views._ticket_thread_view import TicketThreadView
            self.add_view(TicketCreationView())
            self.add_view(TicketThreadView())
            self.__persistent_views_added = True

        await self._sync_voice_users()
        print(f"[{datetime.now().strftime('%c')}]: {self.user}'s ready!")

    async def _sync_voice_users(self) -> None:
        if not settings.API_REQUIRED:
            return

        cog = self.get_cog("VoiceActivityListenerCog")
        for guild in self.guilds:
            for voice_channel in guild.voice_channels:
                for member in voice_channel.members:
                    cog.count_user(member) # type: ignore

    async def sync_user_in_vc(self, member: disnake.Member):
        if not member.voice:
            return
        
        cog = self.get_cog("VoiceActivityListenerCog")
        await cog.sync_user_in_vc(member) # type: ignore

    def _load_cogs(self) -> None:
        cogs_path = settings.COGS_PATH
        test_cogs_path = None
        if settings.DEVELOPMENT:
            test_cogs_path = settings.TEST_COGS_PATH

        _cog_mngr = CogManager(
            cogs_path, test_cogs_path
        )
        for cog in _cog_mngr.cogs:
            self.load_extension(cog)

    async def on_slash_command_error(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        exception: commands.errors.CommandError
    ) -> None:
        await self._on_application_command_error_handler(
            interaction, exception
        )
 
    async def on_user_command_error(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        exception: commands.errors.CommandError
    ) -> None:
        await self._on_application_command_error_handler(
            interaction, exception
        )

    async def on_message_command_error(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        exception: commands.errors.CommandError
    ) -> None:
        await self._on_application_command_error_handler(
            interaction, exception
        )

    async def _on_application_command_error_handler(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        exception: commands.errors.CommandError
    ) -> None:
        if isinstance(exception, commands.CommandNotFound):
            return
        if (isinstance(exception, commands.CommandInvokeError)
            and isinstance(exception.original, CustomException)):
            await interaction.response.send_message(
                embed=ExceptionEmbed(str(exception.original)),
                ephemeral=True
            )
        if isinstance(exception, commands.BadArgument):
            embed = ExceptionEmbed(str(exception))
            if interaction.response.is_done():
                await interaction.followup.send(
                    embed=embed,
                    ephemeral=True)
            else:
                await interaction.response.send_message(
                    embed=embed,
                    ephemeral=True)
        else:
            return await super().on_slash_command_error(interaction, exception)

    async def on_application_command(
        self,
        interaction: disnake.ApplicationCommandInteraction,
    ) -> None:
        options = interaction.data.options
        command_options = ("**Параметры:**\n" +
            "\n".join([f"-# {option['name'].upper()}: **{option['value']}**"
                if option['name'] not in ["member", "участник"] else
                    f"-# {option['name'].upper()}: <@{option['value']}>"
                for option in options
            ])) if len(options) > 0 and options[0].value else ""

        logger.info(
            'Пользователь <@%d> использует команду </%s:%d> в канале <#%d>\n\n%s',
            interaction.author.id,
            interaction.data.name,
            interaction.data.id,
            interaction.channel.id,
            command_options,
            extra={"user_avatar": interaction.user.display_avatar.url, # type: ignore
                    "type": "command_interaction"}
        )
        await super().on_application_command(interaction)

bot = JesterBot()
import disnake
from disnake.ext import commands

from src import _config 
from datetime import datetime
from src._cog_manager import CogManager
from src.logger import get_logger
from src.localization import get_localizator
from src.utils._exceptions import BaseException
from src.utils._embeds import ExceptionEmbed


logger = get_logger()
_ = get_localizator()


class JesterBot(commands.Bot):
    def __init__(self) -> None:
        intents = disnake.Intents.all()
        command_sync_flags = commands.CommandSyncFlags.all()
        command_sync_flags.sync_commands_debug = _config.DEBUG

        super().__init__(
            intents=intents,
            command_sync_flags=command_sync_flags,
            command_prefix="?"
        )
        self.load_cogs()
        self.persistent_views_added = False

    async def on_ready(self) -> None:
        if not self.persistent_views_added:
            from src.cogs.tickets.views._ticket_creation_view import TicketCreationView
            from src.cogs.tickets.views._ticket_thread_view import TicketThreadView
            self.add_view(TicketCreationView())
            self.add_view(TicketThreadView())
            self.persistent_views_added = True
        
        cog = self.get_cog("VoiceActivityListenerCog")
        await cog.sync() # type: ignore

        print(f"[{datetime.now().strftime('%c')}] {self.user}'s ready!")

    def load_cogs(self):
        _cog_mngr = CogManager(_config.COGS_PATH)
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
        if isinstance(exception, BaseException):
            await interaction.response.send_message(
                embed=ExceptionEmbed(str(exception)),
                ephemeral=True
            )
        if isinstance(exception, commands.BadArgument):
            await interaction.response.send_message(
                embed=ExceptionEmbed(str(exception)),
                ephemeral=True
            )
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
            ])) if len(options) > 0 else ""

        logger.info(
            'Пользователь <@%d> использовал команду **/%s** в канале <#%d>\n\n%s',
            interaction.author.id,
            interaction.data.name,
            interaction.channel.id,
            command_options,
            extra={"user_avatar": interaction.user.display_avatar.url, # type: ignore
                    "type": "command_interaction"}
        )
        await super().on_application_command(interaction)

bot = JesterBot()
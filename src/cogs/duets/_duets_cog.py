import asyncio
import disnake
from disnake.ext import commands

from src.bot import JesterBot
from src.logger import get_logger
from src.localization import get_localizator

from src.utils._converters import inter_member
from ._api_interaction import get_duet, become_solo
from .views import ProposalView
from src.utils.ui import BaseEmbed


logger = get_logger()
_ = get_localizator("duets.common")


class DuetsCog(commands.Cog):
    def __init__(self, bot: JesterBot) -> None:
        self._bot = bot
        self.__active_requests = {}

    @commands.slash_command()
    async def duet(
        self,
        interaction: disnake.GuildCommandInteraction
    ) -> None:
        pass

    @duet.sub_command(description=_("duet-create_desc"))
    async def create(
        self,
        interaction: disnake.GuildCommandInteraction,
        duo: disnake.Member = commands.Param(
            converter=inter_member, description=_("duets-create_member_param"))
    ) -> None:
        guild = interaction.guild
        proposer = interaction.user

        if (self.__active_requests.get((guild.id, proposer.id))
            or self.__active_requests.get((guild.id, duo.id))):
            await interaction.response.send_message(
                content=_("duets-already_requested_error"),
                ephemeral=True
            )
            return

        already_busy = await get_duet(guild.id, proposer.id)
        already_taken = await get_duet(guild.id, duo.id)

        if already_busy or already_taken:
            error_message = self._define_error_message((already_busy, already_taken))
            await interaction.response.send_message(
                content=error_message,
                ephemeral=True)
            return

        future = asyncio.Future()
        self.__active_requests[(guild.id, proposer.id)] = future
        self.__active_requests[(guild.id, duo.id)] = future

        view = ProposalView(guild, proposer, duo, future)
        await view.start(interaction)

        try:
            await future
        except asyncio.CancelledError:
            pass
        finally:
            self.__active_requests.pop((guild.id, proposer.id), None)
            self.__active_requests.pop((guild.id, duo.id), None)

    def _define_error_message(self, params: tuple) -> str:
        possible_errors = {
            (True, True): "duets-both_busy_error",
            (True, False): "duets-already_taken_error",
            (False, True): "duets-already_busy_error"
        }
        return _(possible_errors[(bool(params[0]), bool(params[1]))])

    @duet.sub_command(description=_("duet-dispose_desc"))
    async def dispose(
        self,
        interaction: disnake.GuildCommandInteraction
    ) -> None:
        guild = interaction.guild
        user = interaction.user

        has_duet = await get_duet(guild.id, user.id)

        if not has_duet:
            await interaction.response.send_message(
                content=_("duets-already_solo_error"),
                ephemeral=True)
            return

        await become_solo(guild.id, user.id)
        await interaction.response.send_message(
            embed = BaseEmbed(
                title=_("duets-solo_embed_title"),
                description=_("duets-solo_embed_desc", user=user.mention)
            ) 
        )

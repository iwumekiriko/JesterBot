import disnake
from disnake.ext import commands

from src.bot import JesterBot
from src.utils._convertes import bot_excluding
from ._api_interaction import get_member
from src.utils._embeds import BaseEmbed
from src.localization import get_localizator
from src.utils._experience import get_level_from_exp
from src.utils._time import seconds_to_hms


_ = get_localizator("profile")


class ProfileCog(commands.Cog):
    def __init__(self, bot: JesterBot) -> None:
        self.bot = bot

    @commands.slash_command()
    async def profile(
        self,
        interaction: disnake.GuildCommandInteraction,
        member: disnake.Member=commands.Param(converter=bot_excluding, default=None) 
    ) -> None:
        await interaction.response.defer()

        guild = interaction.guild
        if not member:
            member = interaction.author

        member_data = await get_member(member.id, guild.id)
        await interaction.followup.send(
            embed = BaseEmbed(
                title = _("profile_embed_title", username=member.display_name),
                description = _(
                    "profile_embed_desc",
                    exp=member_data.experience,
                    coins=member_data.coins,
                    level=get_level_from_exp(member_data.experience), # type: ignore
                    messages=member_data.message_count,
                    voice_time=seconds_to_hms(member_data.voice_time) # type: ignore
                )
            ).set_thumbnail(member.display_avatar.url)
        )
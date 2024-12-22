import disnake
from disnake.ext import commands

from src.bot import JesterBot
from src.utils._convertes import bot_excluding
from ._api_interaction import get_member
from src.utils.ui import BaseEmbed
from src.localization import get_localizator
from src.utils._experience import get_level_from_exp
from src.utils._time import seconds_to_hms


_ = get_localizator("members-profile")


class ProfileCog(commands.Cog):
    def __init__(self, bot: JesterBot) -> None:
        self.bot = bot

    @commands.slash_command(description=_("profile_desc"))
    async def profile(
        self,
        interaction: disnake.GuildCommandInteraction,
        member: disnake.Member=commands.Param(
            converter=bot_excluding, default=None, description=_("profile_member_param")) 
    ) -> None:
        await interaction.response.defer()

        guild = interaction.guild
        if not member:
            member = interaction.author
        await self.bot.sync_user_in_vc(member)

        member_data = await get_member(guild.id, member.id)
        await interaction.followup.send(
            embed = BaseEmbed(
                title = _("members_profile_embed_title", username=member.display_name),
                description = _(
                    "members_profile_embed_desc",
                    exp=member_data.experience,
                    coins=member_data.coins,
                    level=get_level_from_exp(member_data.experience), # type: ignore
                    messages=member_data.message_count,
                    voice_time=seconds_to_hms(member_data.voice_time) # type: ignore
                )
            ).set_thumbnail(member.display_avatar.url)
        )
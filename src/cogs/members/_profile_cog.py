import disnake
from disnake.ext import commands

from src.bot import JesterBot
from src.utils._converters import bot_excluding
from ._api_interaction import get_member
from src.utils.ui import BaseEmbed
from src.localization import get_localizator
from src.utils._experience import get_level_from_exp
from src.utils._time import seconds_to_hms, make_discord_timestamp
from src.cogs.duets._api_interaction import get_duet
from src.cogs.inventory._api_interaction import get_active_booster
from src.utils.enums import Currency


_ = get_localizator("members.profile")


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
        from src.config import cfg

        await interaction.response.defer()

        guild = interaction.guild
        if not member:
            member = interaction.author
        await self.bot.sync_user_in_vc(member)

        member_data = await get_member(guild.id, member.id)
        def_currency_icon = Currency.COINS.get_icon(member.guild.id)
        donate_currency_icon = Currency.CRYSTALS.get_icon(member.guild.id)

        embed = BaseEmbed(
                title = _("members-profile_embed_title", username=member.display_name),
                description = _(
                    "members-profile_embed_desc",
                    exp=member_data.experience,
                    coins_name=Currency.COINS.guild_short_name,
                    coins=f"{member_data.coins} {def_currency_icon}",
                    crystals_name=Currency.CRYSTALS.guild_short_name,
                    crystals=f"{member_data.crystals} {donate_currency_icon}",
                    level=get_level_from_exp(member_data.experience), # type: ignore
                    messages=member_data.message_count,
                    voice_time=seconds_to_hms(member_data.voice_time) # type: ignore
                )
            ).set_thumbnail(member.display_avatar.url)
        
        active_booster = member_data.active_exp_booster

        if active_booster and active_booster.activated_at:
            embed.add_field(
                name=_("members-profile_bonuses"),
                value = _("members-profile_active_booster",
                          value=active_booster.value,
                          timestamp=make_discord_timestamp(
                              active_booster.activated_at + 
                              active_booster.duration # type: ignore
                          )),
                inline=True
            )

        duet = member_data.duet

        if duet is not None:
            embed.add_field(
                name=_("members-profile_extra_info"),
                value=_("members-profile_duet_with", 
                        proposer=duet.proposer_id, duo=duet.duo_id,
                        together_from=disnake.utils.format_dt(duet.together_from)),
                inline=False
            )

        await interaction.followup.send(embed=embed)

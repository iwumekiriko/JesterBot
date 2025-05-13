from enum import Enum

import disnake
from disnake.ext import commands

from src.bot import JesterBot
from src.localization import get_localizator

from ._api_interaction import get_top
from src.utils._converters import bot_excluding
from src.utils.ui import BaseEmbed
from src.utils._time import make_discord_timestamp, seconds_to_hms
from src.utils.enums import Currency


_ = get_localizator("top")


TOP_AMOUNT = 10


class TopTypes(str, Enum):
    MESSAGES = 1
    VOICE = 2
    EXPERIENCE = 3
    CURRENCY = 4
    LOOTBOXES = 5
    QUESTS = 6
    DUETS = 7

    @property
    def translated(self) -> str:
        return _(f"top-{self.name.lower()}_type")
    
    def format_stats(self, user_id: int, guild_id: int, stats: dict) -> str:
        formatters = {
            TopTypes.MESSAGES: lambda s: _(f"messages_top_format",
                user = user_id,
                messages = s['messagesWritenCount']
            ),
            TopTypes.VOICE: lambda s: _(f"voice_top_format",
                user = user_id,
                muted=seconds_to_hms(s['voiceTimeMuted']), 
                unmuted=seconds_to_hms(s['voiceTimeUnMuted'])
            ),
            TopTypes.EXPERIENCE: lambda s: _(f"experience_top_format",
                user = user_id,
                experience = s['experience']
            ),
            TopTypes.CURRENCY: lambda s: _(f"currency_top_format",
                user = user_id,
                coins=s['coins'],
                coins_icon=Currency.COINS.get_icon(guild_id),
                crystals=s['crystals'],
                crystals_icon=Currency.CRYSTALS.get_icon(guild_id)
            ),
            TopTypes.LOOTBOXES: lambda s: _(f"lootboxes_top_format",
                user = user_id,
                lootboxes = s['allLootboxesOpenedCount']
            ),
            TopTypes.QUESTS: lambda s: _(f"quests_top_format",
                user = user_id,
                quests = s['questsCompletedCount']
            ),
            TopTypes.DUETS: lambda s: _(f"duest_top_format",
                proposer=s['proposerId'],
                duo=s['duoId'],
                together_from=make_discord_timestamp(s['togetherFrom'])
            )
        }
        return formatters[self](stats)


class TopCog(commands.Cog):
    def __init__(self, bot: JesterBot) -> None:
        self.bot = bot

    @commands.slash_command(description=_("top_desc"))
    async def top(
        self,
        interaction: disnake.GuildCommandInteraction,
        type=commands.Param(
            choices={ type.translated: type for type in TopTypes }, description=_("top-type_param")),
        member: disnake.Member=commands.Param(description=_("top-member_param"), default=None, converter=bot_excluding)
    ) -> None:
        requested_user_id = member.id if isinstance(member, disnake.Member) else interaction.user.id
        guild_id = interaction.guild.id
        top_type = TopTypes(type)

        top_data = await get_top(
            guild_id,
            requested_user_id,
            top_type.value
        )

        data = []
        is_user_in_top = False
        user_info = top_data['requestedUser']

        for user in top_data['top']:
            stats_str = top_type.format_stats(user['userId'], guild_id, user['stats'])
            
            is_duet_user = False
            if top_type == TopTypes.DUETS:
                is_duet_user = requested_user_id in {user['stats']['proposerId'], user['stats']['duoId']}
            
            line = f"{user['rank']}。{stats_str}"
            if user['userId'] == requested_user_id or is_duet_user:
                line = f"**{line}**"
                is_user_in_top = True
            
            data.append(line)

        if not is_user_in_top:
            user_stats = (top_type.format_stats(user_info['userId'], guild_id, user_info['stats'])
                           if user_info['stats'] else _("data_not_found", user=user_info['userId']))
            data.append(f"———————————————————\n\n**{user_info['rank']}。{user_stats}**")

        await interaction.response.send_message(
            embed=BaseEmbed(
                title=top_type.translated,
                description="\n".join(data)
            )
        )


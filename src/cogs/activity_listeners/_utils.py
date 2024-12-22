import disnake

from src.models import Member
from src.utils._experience import get_level_from_exp
from src.utils.ui import BaseEmbed
from src.localization import get_localizator


_ = get_localizator("activity_listeners")


REWARD_MESSAGE_DELETE_AFTER = 30


async def send_reward_message(
    member: Member,
    channel: disnake.TextChannel | disnake.Thread | int,
    reward: int
) -> None:
    if not member.experience:
        return
    
    guild_channel = channel
    if isinstance(channel, int):
        from src.bot import bot
        guild_channel = bot.get_channel(channel)

    level_after = get_level_from_exp(member.experience)
    level_before = level_after - 1

    if not isinstance(guild_channel, 
        (disnake.TextChannel, disnake.Thread)):
        return

    await guild_channel.send(content=f"<@{member.user_id}>",
        embed = BaseEmbed(
            title=_("activity_listeners_reward_embed_title"),
            description=_(
                "activity_listeners_reward_embed_desc",
                level_before=level_before,
                level_after=level_after,
                rewards=reward
            )
        ), delete_after=REWARD_MESSAGE_DELETE_AFTER )
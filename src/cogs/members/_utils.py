import disnake

from src.models import Member
from src.utils._experience import get_level_from_exp
from src.utils.ui import BaseEmbed
from src.localization import get_localizator


_ = get_localizator("activity")


# REWARD_MESSAGE_DELETE_AFTER = 30


async def send_reward_message(
    member: Member,
    reward: int
) -> None:
    if member.experience is None:
        return
    
    from src.config import cfg
    from src.bot import bot

    offtop_channel_id = cfg.channels_cfg(member.guild_id).offtop_channel_id
    if not offtop_channel_id:
        return

    offtop_channel = bot.get_channel(offtop_channel_id)
    if not isinstance(offtop_channel, disnake.TextChannel):
        return

    level_after = get_level_from_exp(member.experience)
    level_before = level_after - 1

    await offtop_channel.send(content=f"<@{member.user_id}>",
        embed = BaseEmbed(
            title=_("activity_listeners_reward_embed_title"),
            description=_(
                "activity_listeners_reward_embed_desc",
                level_before=level_before,
                level_after=level_after,
                rewards=reward
            )
        ))
import random

import disnake
from disnake.ext import commands

from src.utils._events import CustomEvents
from src.customisation import NITRO_BOOSTING_GRATITUDERS
from ..embeds import NitroBoostingEmbed

from src.bot import JesterBot
from src.logger import get_logger


logger = get_logger()


class NitroBoostingActivityListenerCog(commands.Cog):
    def __init__(self, bot: JesterBot):
        self._bot = bot

    @commands.Cog.listener(f'on_{CustomEvents.GUILD_NITRO_BOOSTED}')
    async def on_guild_nitro_boosted(
        self,
        member: disnake.Member,
    ) -> None:
        logger.info("%d nitro boosted the server %d", member.id, member.guild.id)
        from src.config import cfg
        channels_cfg = cfg.channels_cfg(member.guild.id)

        if not (nbci := channels_cfg.nitro_boosting_channel_id):
            logger.warning("can not find nitro boosting channel id in config")
            return

        nitro_boosting_channel = member.guild.get_channel(nbci)
        if not isinstance(nitro_boosting_channel, disnake.TextChannel):
            logger.warning("nitro boosting channel is not text channel")
            return

        gratituder_name = random.choice(list(NITRO_BOOSTING_GRATITUDERS.keys()))
        gratituder_avatar, gratituder_texts = NITRO_BOOSTING_GRATITUDERS[gratituder_name]

        gratitude_text = random.choice(gratituder_texts)

        webhook = next((
            wh for wh in await nitro_boosting_channel.webhooks() 
            if wh.name == gratituder_name), None)
        if not webhook:
            webhook = await nitro_boosting_channel.create_webhook(name=gratituder_name)

        await webhook.send(
            avatar_url=gratituder_avatar,
            username=gratituder_name,
            content=member.mention,
            embed=NitroBoostingEmbed(
                description=gratitude_text
            ),
        )

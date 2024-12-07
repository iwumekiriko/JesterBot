import re
import disnake
from disnake.ext import commands

from src.bot import JesterBot
from src.localization import get_localizator
from src.logger import get_logger
from ._api_interaction import add_experience, add_coins
from src.utils._experience import get_level_from_exp
from src.models import Member
from src.utils._embeds import BaseEmbed


_ = get_localizator("activity")
logger = get_logger()


REWARD_MESSAGE_DELETE_AFTER = 30


class TextActivityListenerCog(commands.Cog):
    def __init__(self, bot: JesterBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message) -> None:
        author = message.author
        channel = message.channel

        if not isinstance(author, disnake.Member):
            return
        
        if not isinstance(channel, disnake.TextChannel):
            return
        
        if author.bot:
            return
        
        await self._check_for_reaction_messages(message)
        await _give_exp_for_message(author, channel)

    async def _check_for_reaction_messages(
            self, message: disnake.Message
    ) -> None:
        if len(re.findall(r"\b{}\b".format("мяу"), message.content.lower())) > 0:
            await message.add_reaction("<a:zlozlozlozlozlozlozlozlozlozlo:1299735705148330097>")

        if len(re.findall(r"\b{}\b".format("фыр"), message.content.lower())) > 0:
            await message.add_reaction("<:kwolik:1302188971270344826>")

        if len(re.findall(r"\b{}\b".format("хрю"), message.content.lower())) > 0:
            await message.add_reaction("🐖")

        if len(re.findall(r"\b{}\b".format("кря"), message.content.lower())) > 0:
            await message.add_reaction("🦆")

        if self.bot.user.mention in message.content:
            await message.add_reaction("🤡")

    @commands.Cog.listener()
    async def on_message_edit(
        self,
        before: disnake.Message,
        after: disnake.Message
    ) -> None:
        if before.author.bot:
            return
        
        if before.content == after.content:
            return

        logger.warning(
            "Пользователь <@%d> изменил сообщение [%s].\n\n**До: **\n```%s```\n**После: **\n```%s```\n-# ID сообщения: %d",
            before.author.id, after.jump_url, before.content, after.content, after.id,
            extra={ "user_avatar": before.author.display_avatar.url, "type": "message" }) # type: ignore
        
    @commands.Cog.listener()
    async def on_message_delete(self, message: disnake.Message) -> None:
        if message.author.bot:
            return

        logger.warning(
            "Пользователь <@%d> удалил сообщение!\n\n**Текст сообщения: \n**```%s```\n-# ID сообщения: %d",
            message.author.id, message.content, message.id,
            extra={ "user_avatar": message.author.display_avatar.url, "type": "message", "images": [attch.url for attch in message.attachments] }) # type: ignore


async def _give_exp_for_message(
    author: disnake.Member,
    channel: disnake.TextChannel    
) -> None:
    member = await add_experience(author)
    if _is_new_lvl(member):
        await add_coins(member)
        await _send_reward_message(member, channel)


def _is_new_lvl(member: Member) -> bool:
    from src.config import cfg

    if not member.experience:
        return False
    
    exp_for_message = cfg.exp_cfg(member.guild_id).exp_for_message
    if not exp_for_message:
        return False

    exp_before = member.experience - exp_for_message
    exp_after = member.experience

    level_before = get_level_from_exp(exp_before)
    level_after = get_level_from_exp(exp_after)

    return True if level_before < level_after else False


async def _send_reward_message(member: Member, channel: disnake.TextChannel) -> None:
    if not member.experience:
        return

    level_after = get_level_from_exp(member.experience)
    level_before = level_after - 1

    await channel.send(content=f"<@{member.user_id}>",
        embed = BaseEmbed(
            title=_("reward_embed_title"),
            description=_(
                "reward_embed_desc",
                level_before=level_before,
                level_after=level_after,
                rewards=300
            )
        ), delete_after=REWARD_MESSAGE_DELETE_AFTER )

import re

import disnake
from disnake.ext import commands

from src.bot import JesterBot
from src.localization import get_localizator
from src.logger import get_logger
from .._api_interaction import add_message_experience
from src.cogs.economy._api_interaction import update_member_coins
from .._utils import send_reward_message, check_for_mod_actions
from src.utils._experience import is_new_lvl, ExpTypes
from src.utils._text import prepare_block_text
from src.settings import API_REQUIRED

_ = get_localizator("activity")
logger = get_logger()


class TextActivityListenerCog(commands.Cog):
    def __init__(self, bot: JesterBot):
        self._bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message) -> None:
        author = message.author
        channel = message.channel

        if not isinstance(author, disnake.Member):
            return

        if (not isinstance(channel, disnake.TextChannel)
            and not isinstance(channel, disnake.Thread)):
            return

        if author.bot:
            return

        await _give_exp_for_message(author)
        await self._check_for_reaction_messages(message)

    async def _check_for_reaction_messages(
        self, message: disnake.Message
    ) -> None:
        reactions = {
            r"\bмяу\b": "<a:zlozlozlozlozlozlozlozlozlozlo:1299735705148330097>",
        }

        lower_content = message.content.lower()
        for keyword, reaction in reactions.items():
            if re.search(keyword, lower_content):
                await message.add_reaction(reaction)

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
            "Пользователь <@%d> изменяет сообщение [%s].\n\n**До: **\n%s\n**После: **\n%s\n-# ID сообщения: %d",
            before.author.id, after.jump_url,
            prepare_block_text(before.content), prepare_block_text(after.content), after.id,
            extra={
                "user_avatar": before.author.display_avatar.url,
                "type": "message",
                "guild_id": before.guild.id # type: ignore
            })

    @commands.Cog.listener()
    async def on_message_delete(self, message: disnake.Message) -> None:
        if message.author.bot:
            return

        deleted_by = await check_for_mod_actions(
            guild=message.guild, # type: ignore
            action=disnake.AuditLogAction.message_delete,
            user_id=message.author.id
        )

        warning_message = (f"Сообщение от <@{message.author.id}> было удалено из канала [{message.channel.jump_url}]"
                           f"\n\n**Текст сообщения: \n**{prepare_block_text(message.content)}")
        if deleted_by:
            warning_message += f"\n**Модератор:** {deleted_by.mention}"
        warning_message += f"\n\n-# ID сообщения: {message.id}"

        logger.warning(
            warning_message,
            extra={
                "user_avatar": message.author.display_avatar.url,
                "type": "message",
                "guild_id": message.guild.id # type: ignore
            }
        )


async def _give_exp_for_message(author: disnake.Member) -> None:
    if not API_REQUIRED:
        return

    member = await add_message_experience(author)
    is_lvled, coins = is_new_lvl(member, ExpTypes.MESSAGE)
    if is_lvled:
        await update_member_coins(member.guild_id, member.user_id, coins)
        await send_reward_message(member, coins)

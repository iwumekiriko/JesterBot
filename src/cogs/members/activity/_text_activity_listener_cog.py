import re

import disnake
from disnake.ext import commands

from src.bot import JesterBot
from src.localization import get_localizator
from src.logger import get_logger
from .._api_interaction import add_message_experience
from src.cogs.economy._api_interaction import proceed_coins_reward
from .._utils import send_reward_message, check_for_mod_actions
from src.utils._experience import check_if_new_lvl, ExpTypes
from src.utils._text import prepare_block_text
from src.settings import API_REQUIRED


_ = get_localizator("members.activity")
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

        await _give_exp_for_message(author, channel.id)
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

        images_urls = []
        if before.attachments != after.attachments:
            images_urls = await self._get_message_images_urls(before, after)

        if before.content == after.content:
            if not len(images_urls) > 0:
                return

        logger.warning(
            "Пользователь <@%d> изменяет сообщение [%s].\n\n**До: **\n%s\n**После: **\n%s\n-# ID сообщения: %d",
            before.author.id, after.jump_url,
            prepare_block_text(before.content), prepare_block_text(after.content), after.id,
            extra={
                "user_avatar": await self._bot.save_avatar(before.author),
                "type": "message",
                "guild_id": before.guild.id, # type: ignore
                "images_urls": images_urls
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

        warning_message = (f"Сообщение от <@{message.author.id}> было удалено из канала [{message.channel.jump_url}]" # type: ignore
                           f"\n\n**Текст сообщения: \n**{prepare_block_text(message.content)}")
        if deleted_by:
            warning_message += f"\n**Модератор:** {deleted_by.mention}"
        warning_message += f"\n\n-# ID сообщения: {message.id}"

        images_urls = await self._get_message_images_urls(message)

        logger.warning(
            warning_message,
            extra={
                "user_avatar": await self._bot.save_avatar(message.author),
                "type": "message",
                "guild_id": message.guild.id, # type: ignore
                "images_urls": images_urls
            }
        )

    async def _get_message_images_urls(self, message: disnake.Message, diff_from: disnake.Message | None = None) -> list:
        images_urls = []

        exclude_ids = {attach.id for attach in diff_from.attachments} if diff_from else set()

        for attach in message.attachments:
            if attach.content_type in ["image/png", "image/jpg", "image/jpeg", "image/webp"]:
                if attach.id not in exclude_ids:
                    file = await attach.to_file()
                    url = await self._bot.save_file(message.guild.id, file) # type: ignore
                    images_urls.append(url)

        return images_urls


    async def _get_message_files_urls(self, message: disnake.Message) -> list:
        ...


async def _give_exp_for_message(author: disnake.Member, channel_id: int) -> None:
    if not API_REQUIRED:
        return

    if author.bot:
        return

    member = await add_message_experience(author, channel_id)
    is_lvled, coins = check_if_new_lvl(member, ExpTypes.MESSAGE)
    if is_lvled:
        await proceed_coins_reward(member.guild_id, member.user_id, coins)
        await send_reward_message(member, coins)

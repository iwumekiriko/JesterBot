import random
import disnake
from disnake.ext import commands

from src.bot import JesterBot
from src.localization import get_localizator
from src.logger import get_logger
from src.cogs.members._api_interaction import get_member


_ = get_localizator("activity")
logger = get_logger()


MIN_EXP_PER_MESSAGE = 1
MAX_EXP_PER_MESSAGE = 2


class TextActivityListenerCog(commands.Cog):
    def __init__(self, bot: JesterBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message) -> None:
        author = message.author
        channel = message.channel
        
        if message.content == "мяу" and not author.bot:
            await channel.send(_("meow"))

        exp = random.randint(MIN_EXP_PER_MESSAGE, MAX_EXP_PER_MESSAGE)
        await _give_exp_for_message(author.id, exp)

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
            extra={ "user_avatar": message.author.display_avatar.url, "type": "message" })# type: ignore

async def _give_exp_for_message(
    author_id: int,
    exp: int
) -> None:
    pass
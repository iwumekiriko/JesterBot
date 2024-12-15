import re
import disnake
from disnake.ext import commands

from src.bot import JesterBot
from src.localization import get_localizator
from src.logger import get_logger
from ._api_interaction import add_experience, add_coins
from ._utils import send_reward_message
from src.utils._experience import is_new_lvl
from src.utils._text import prepare_block_text

_ = get_localizator("activity")
logger = get_logger()


class TextActivityListenerCog(commands.Cog):
    def __init__(self, bot: JesterBot):
        self.bot = bot

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
        
        await _give_exp_for_message(author, channel)
        await self._check_for_reaction_messages(message)

    async def _check_for_reaction_messages(
        self, message: disnake.Message
    ) -> None:
        reactions = {
            r"\bмяу\b": "<a:zlozlozlozlozlozlozlozlozlozlo:1299735705148330097>",
            r"\bфыр\b": "<:kwolik:1302188971270344826>",
            r"\bхрю\b": "🐖",
            r"\bкря\b": "🦆",
            r"\bгав\b": "<:z_proebali:1313506419185549433>",
            r"\bгол\b": "<:k_GOAL:1313506931259871292>",
        }
        lower_content = message.content.lower()
        for keyword, reaction in reactions.items():
            if re.search(keyword, lower_content):
                await message.add_reaction(reaction)

        if self.bot.user.mention in message.content:
            await message.add_reaction("<:joe_artem:1314324435271946260>")

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
            extra={ "user_avatar": before.author.display_avatar.url, "type": "message" }) # type: ignore
        
    @commands.Cog.listener()
    async def on_message_delete(self, message: disnake.Message) -> None:
        if message.author.bot:
            return
        
        logger.warning(
            "Сообщение от <@%d> было удалено\n\n**Текст сообщения: \n**%s\n-# ID сообщения: %d",
            message.author.id, prepare_block_text(message.content), message.id,
            extra={ "user_avatar": message.author.display_avatar.url, "type": "message" }) # type: ignore


async def _give_exp_for_message(
    author: disnake.Member,
    channel: disnake.TextChannel | disnake.Thread    
) -> None:
    member = await add_experience(author)
    if is_new_lvl(member, "message"):
        await add_coins(member)
        await send_reward_message(member, channel)

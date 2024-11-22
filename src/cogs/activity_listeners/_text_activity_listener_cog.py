import random
import disnake
from disnake.ext import commands

from src.bot import JesterBot
from src.localization import get_localizator


_ = get_localizator("activity")


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


async def _give_exp_for_message(
    author_id: int,
    exp: int
) -> None:
    pass
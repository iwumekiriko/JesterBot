import disnake
from disnake.ext import commands

from src.bot import JesterBot
from src.localization import get_localizator


_ = get_localizator("activity")


class ActivityListenerCog(commands.Cog):
    def __init__(self, bot: JesterBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message) -> None:
        if message.content == "мяу" and not message.author.bot:
            await message.channel.send(_("meow"))
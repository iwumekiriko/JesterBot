import disnake
from disnake.ext import commands

from src.bot import JesterBot
from src.utils._convertes import inter_member
from src.localization import get_localizator
from src.utils._embeds import BaseEmbed
from .views._shop_creation_view import ShopCreationView
from src.logger import get_logger


logger = get_logger()


class ShopCog(commands.Cog):
    def __init__(self, bot: JesterBot):
        self._bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        shop_channel = self._bot.get_channel(1243676507772026920)
        if not isinstance(shop_channel, disnake.TextChannel):
            logger.error("channel for shop is not setted")
            return
        
        try:
            await shop_channel.fetch_message(1243676507772026920)
        except:
            view = ShopCreationView()
            await shop_channel.send(
                embed=view.create_embed(),
                view=view
            )
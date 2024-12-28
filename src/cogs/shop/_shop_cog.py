import disnake
from disnake.ext import commands

from src.bot import JesterBot
from src.utils._embeds import BaseEmbed
from .views._shop_creation_view import ShopCreationView
from src.logger import get_logger
from src.models.config import ShopConfig
from src.utils._convertes import user_avatar


logger = get_logger()


class ShopCog(commands.Cog):
    def __init__(self, bot: JesterBot):
        self._bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        from src.config import cfg

        for guild in self._bot.guilds:
            # shop_cfg: ShopConfig = cfg.config[guild.id]["Shop"]
            shop_channel_id = 1243676507772026920
            shop_message_id = 1
            if not shop_channel_id:
                return

            shop_channel = self._bot.get_channel(shop_channel_id)
            if not isinstance(shop_channel, disnake.TextChannel):
                logger.debug("Канал для магазиника недоступен!",
                            extra={"user_avatar": user_avatar(jester=True),
                                    "type": "else"})
                return
            
            try:
                await shop_channel.fetch_message(shop_message_id) # type: ignore
            except:
                view = ShopCreationView()
                message = await shop_channel.send(
                    embed=view.create_embed(),
                    view=view
                )
                view.message = message
                logger.info("Тикет сообщение не было найдено. Создано новое.",
                            extra={"user_avatar": user_avatar(jester=True), 
                                   "type": "else", "guild_id": shop_channel.guild.id})
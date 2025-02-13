import disnake
from disnake.ext import commands

from src.bot import JesterBot
from .views import TicketCreationView
from src.utils._converters import user_avatar
from src.logger import get_logger
from ._api_interaction import set_ticket_message


logger = get_logger()


class TicketsCog(commands.Cog):
    def __init__(self, bot: JesterBot):
        self._bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        from src.config import cfg

        for guild in self._bot.guilds:
            ticket_cfg = cfg.tickets_cfg(guild.id)
            ticket_channel_id = ticket_cfg.ticket_channel_id
            ticket_message_id = ticket_cfg.ticket_message_id

            if not ticket_channel_id:
                return

            ticket_channel = self._bot.get_channel(ticket_channel_id)
            if not isinstance(ticket_channel, disnake.TextChannel):
                logger.debug("Канал для тикетов недоступен!",
                            extra={"user_avatar": user_avatar(jester=True),
                                    "type": "else"})
                return
            
            try:
                await ticket_channel.fetch_message(ticket_message_id) # type: ignore
            except:
                view = TicketCreationView()
                message = await ticket_channel.send(
                    embed=view.create_embed(),
                    view=view
                )
                logger.info("Тикет сообщение не было найдено. Создано новое.",
                            extra={"user_avatar": user_avatar(jester=True), 
                                   "type": "else", "guild_id": ticket_channel.guild.id})
                await set_ticket_message(guild.id, message.id)

        


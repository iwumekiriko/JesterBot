import disnake
from disnake.ext import commands

from src.bot import JesterBot
from .views._ticket_creation_view import TicketCreationView
from src.utils._convertes import user_avatar
from src.logger import get_logger
from src._config import TICKET_CHANNEL_ID, TICKET_MESSAGE_ID


logger = get_logger()


class TicketsCog(commands.Cog):
    def __init__(self, bot: JesterBot):
        self._bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        ticket_channel = self._bot.get_channel(TICKET_CHANNEL_ID)
        if not isinstance(ticket_channel, disnake.TextChannel):
            logger.debug("Канал для тикетов недоступен!",
                          extra={"user_avatar": user_avatar(jester=True),
                                 "type": "else"})
            return
        
        try:
            await ticket_channel.fetch_message(TICKET_MESSAGE_ID)
        except:
            view = TicketCreationView()
            await ticket_channel.send(
                embed=view.create_embed(),
                view=view
            )

        


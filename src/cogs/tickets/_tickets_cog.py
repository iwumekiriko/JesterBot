import disnake
from disnake.ext import commands

from src.bot import JesterBot
from .views._ticket_creation_view import TicketCreationView
from src.logger import get_logger
from src._config import TICKET_CHANNEL, TICKET_MESSAGE


logger = get_logger()


class TicketsCog(commands.Cog):
    def __init__(self, bot: JesterBot):
        self._bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        ticket_channel = self._bot.get_channel(TICKET_CHANNEL)
        if not isinstance(ticket_channel, disnake.TextChannel):
            logger.error("channel for tickets is not setted")
            return
        
        try:
            await ticket_channel.fetch_message(TICKET_MESSAGE)
        except:
            view = TicketCreationView()
            await ticket_channel.send(
                embed=view.create_embed(),
                view=view
            )

        


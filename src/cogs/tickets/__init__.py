from src.bot import JesterBot
from ._tickets_cog import TicketsCog
from src.settings import API_REQUIRED


def setup(bot: JesterBot) -> None:
    if not API_REQUIRED:
        return

    bot.add_cog(TicketsCog(bot))
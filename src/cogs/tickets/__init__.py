from src.bot import JesterBot
from ._tickets_cog import TicketsCog


def setup(bot: JesterBot) -> None:
    bot.add_cog(TicketsCog(bot))
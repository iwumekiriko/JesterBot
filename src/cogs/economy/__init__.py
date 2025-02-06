from src.bot import JesterBot
from ._economy_cog import EconomyCog


def setup(bot: JesterBot) -> None:
    bot.add_cog(EconomyCog(bot))
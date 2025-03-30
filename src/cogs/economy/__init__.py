from src.bot import JesterBot
from ._economy_cog import EconomyCog
from src.settings import API_REQUIRED


def setup(bot: JesterBot) -> None:
    if not API_REQUIRED:
        return

    bot.add_cog(EconomyCog(bot))
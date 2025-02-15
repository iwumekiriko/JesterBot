from src.bot import JesterBot
from ._duets_cog import DuetsCog
from src.settings import API_REQUIRED


def setup(bot: JesterBot) -> None:
    if not API_REQUIRED:
        return

    bot.add_cog(DuetsCog(bot))
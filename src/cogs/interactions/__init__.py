from src.bot import JesterBot
from ._interact_cog import UserInteractionsCog
from src.settings import API_REQUIRED


def setup(bot: JesterBot) -> None:
    if not API_REQUIRED:
        return

    bot.add_cog(UserInteractionsCog(bot))
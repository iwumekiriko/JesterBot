from src.bot import JesterBot
from ._interact_cog import UserInteractionsCog


def setup(bot: JesterBot) -> None:
    bot.add_cog(UserInteractionsCog(bot))
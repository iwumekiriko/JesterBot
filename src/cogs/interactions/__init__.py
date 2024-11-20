from src.bot import JesterBot
from ._user_interactions_cog import UserInteractionsCog


def setup(bot: JesterBot) -> None:
    bot.add_cog(UserInteractionsCog(bot))
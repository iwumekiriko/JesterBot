from src.bot import JesterBot
from ._clean_cog import CleanCog


def setup(bot: JesterBot) -> None:
    bot.add_cog(CleanCog(bot))
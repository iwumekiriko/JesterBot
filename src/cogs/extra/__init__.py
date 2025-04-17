from src.bot import JesterBot
from ._dnd_roll_cog import DNDRollCog


def setup(bot: JesterBot) -> None:
    bot.add_cog(DNDRollCog(bot))
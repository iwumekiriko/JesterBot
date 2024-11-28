from src.bot import JesterBot
from ._eval_cog import EvalCog


def setup(bot: JesterBot) -> None:
    bot.add_cog(EvalCog())
from src.bot import JesterBot

from ._views_test_cog import ViewsTestCog


def setup(bot: JesterBot) -> None:
    bot.add_cog(ViewsTestCog(bot))
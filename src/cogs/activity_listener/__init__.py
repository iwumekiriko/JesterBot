from src.bot import JesterBot
from ._activity_listener_cog import ActivityListenerCog


def setup(bot: JesterBot) -> None:
    bot.add_cog(ActivityListenerCog(bot))
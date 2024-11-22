from src.bot import JesterBot
from ._text_activity_listener_cog import TextActivityListenerCog


def setup(bot: JesterBot) -> None:
    bot.add_cog(TextActivityListenerCog(bot))
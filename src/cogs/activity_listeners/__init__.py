from src.bot import JesterBot
from ._text_activity_listener_cog import TextActivityListenerCog
from ._voice_activity_listener_cog import VoiceActivityListenerCog


def setup(bot: JesterBot) -> None:
    bot.add_cog(TextActivityListenerCog(bot))
    bot.add_cog(VoiceActivityListenerCog(bot))
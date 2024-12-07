from src.bot import JesterBot
from ._text_activity_listener_cog import TextActivityListenerCog
from ._voice_activity_listener_cog import VoiceActivityListenerCog
from src.settings import API_REQUIRED


def setup(bot: JesterBot) -> None:
    if not API_REQUIRED:
        return

    bot.add_cog(TextActivityListenerCog(bot))
    bot.add_cog(VoiceActivityListenerCog(bot))
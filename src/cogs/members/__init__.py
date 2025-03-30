from src.bot import JesterBot
from ._on_guild_cog import OnGuildCog
from ._profile_cog import ProfileCog
from .activity._text_activity_listener_cog import TextActivityListenerCog
from .activity._voice_activity_listener_cog import VoiceActivityListenerCog
from src.settings import API_REQUIRED


def setup(bot: JesterBot) -> None:
    bot.add_cog(TextActivityListenerCog(bot))
    bot.add_cog(OnGuildCog(bot))

    if not API_REQUIRED:
        return

    bot.add_cog(ProfileCog(bot))
    bot.add_cog(VoiceActivityListenerCog(bot))
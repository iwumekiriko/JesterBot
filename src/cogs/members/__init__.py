from src.bot import JesterBot
from ._profile_cog import ProfileCog
from .activity._on_guild_activity_cog import OnGuildActivityCog
from .activity._text_activity_listener_cog import TextActivityListenerCog
from .activity._voice_activity_listener_cog import VoiceActivityListenerCog
from .activity._nitro_boosting_activity_listener_cog import NitroBoostingActivityListenerCog
from ._top_cog import TopCog
from src.settings import API_REQUIRED


def setup(bot: JesterBot) -> None:
    bot.add_cog(NitroBoostingActivityListenerCog(bot))
    bot.add_cog(TextActivityListenerCog(bot))
    bot.add_cog(OnGuildActivityCog(bot))

    if not API_REQUIRED:
        return

    bot.add_cog(ProfileCog(bot))
    bot.add_cog(VoiceActivityListenerCog(bot))
    bot.add_cog(TopCog(bot))
from src.bot import JesterBot
from ._on_guild_cog import OnGuildCog
from ._profile_cog import ProfileCog
from src.settings import API_REQUIRED


def setup(bot: JesterBot) -> None:
    if not API_REQUIRED:
        return

    bot.add_cog(ProfileCog(bot))
    bot.add_cog(OnGuildCog(bot))
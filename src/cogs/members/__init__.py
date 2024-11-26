from src.bot import JesterBot
from ._on_guild_cog import OnGuildCog
from ._profile_cog import ProfileCog


def setup(bot: JesterBot) -> None:
    bot.add_cog(ProfileCog(bot))
    bot.add_cog(OnGuildCog(bot))
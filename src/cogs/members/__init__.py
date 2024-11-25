from src.bot import JesterBot
from ._on_guild_cog import OnGuildCog


def setup(bot: JesterBot) -> None:
    bot.add_cog(OnGuildCog(bot))
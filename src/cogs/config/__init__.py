from src.bot import JesterBot
from ._config_cog import ConfigCog
from src.settings import API_REQUIRED


def setup(bot: JesterBot) -> None:
    if not API_REQUIRED:
        return

    bot.add_cog(ConfigCog(bot))
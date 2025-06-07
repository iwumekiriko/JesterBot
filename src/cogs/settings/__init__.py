from ._settings_cog import SettingsCog
from src.bot import JesterBot

from src.settings import API_REQUIRED


def setup(bot: JesterBot) -> None:
    if not API_REQUIRED:
        return

    bot.add_cog(SettingsCog(bot))
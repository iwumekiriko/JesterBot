from src.bot import JesterBot
from ._lootboxes_cog import LootboxesCog
from src.settings import API_REQUIRED


def setup(bot: JesterBot) -> None:
    if not API_REQUIRED:
        return

    bot.add_cog(LootboxesCog(bot))
from src.bot import JesterBot
from ._inventory_cog import InventoryCog
from src.settings import API_REQUIRED


def setup(bot: JesterBot) -> None:
    if not API_REQUIRED:
        return

    bot.add_cog(InventoryCog(bot))
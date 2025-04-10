from src.bot import JesterBot
from ._shop_cog import ShopCog
from src.settings import API_REQUIRED


def setup(bot: JesterBot) -> None:
    if not API_REQUIRED:
        return

    bot.add_cog(ShopCog(bot))
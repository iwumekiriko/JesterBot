from src.bot import JesterBot
from ._shop_cog import ShopCog


def setup(bot: JesterBot) -> None:
    bot.add_cog(ShopCog(bot))
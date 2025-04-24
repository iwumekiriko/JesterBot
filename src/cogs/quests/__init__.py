from ._quests_cog import QuestsCog
from src.bot import JesterBot


def setup(bot: JesterBot) -> None:
    bot.add_cog(QuestsCog(bot))
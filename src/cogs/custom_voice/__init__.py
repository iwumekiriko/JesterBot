from src.bot import JesterBot
from ._custom_voice_cog import CustomVoiceCog


def setup(bot: JesterBot) -> None:
    bot.add_cog(CustomVoiceCog(bot))
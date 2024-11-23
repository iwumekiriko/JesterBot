from src.bot import bot
from src._config import BOT_TOKEN
from src.logger import setup_logger

if __name__ == "__main__":
    setup_logger()
    bot.run(BOT_TOKEN)
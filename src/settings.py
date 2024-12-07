from dotenv import load_dotenv
import os

load_dotenv()

APP_NAME = "JesterBot"
DEBUG = True
COGS_PATH = "src/cogs"
API_REQUIRED = True

BOT_TOKEN = os.getenv("BOT_TOKEN")
TENOR_API_KEY = os.getenv("TENOR_API_KEY")
PATH_TO_API: str = os.getenv("PATH_TO_API") # type: ignore
BASE_GUILD_ID = 1296417944934285313
from dotenv import load_dotenv
import os

load_dotenv()

APP_NAME = "JesterBot"
DEVELOPMENT = False
DEBUG = True
COGS_PATH = "src/cogs"
TEST_COGS_PATH = "tests/cogs"

# This type of project is divided by two parts:
# Python code is responsible for user interactions and any types of calculations
# REST API is required for database interactions

# In case there is no API -> set API_REQUIRED setting to False.
# * Optionally [configuration params] can be filled in 'manual_config.py'.
API_REQUIRED = True

# If webhook configuration wasn't filled (doesn't matter manually or through API) \
# Logger will send a warning after each action.
# To disable this -> set SUPPRESS_WEBHOOK_CONFIGURATION to True.
SUPPRESS_WEBHOOK_CONFIGURATION = False


# --------------------------------------------------------------------------------


# Main part of the bot -> TOKEN
# Setted in .env as this is secret key.
# https://discord.com/developers/applications/ -> Your Application -> Bot -> Reset Token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Will not be needed in the future.
# Currently used in /user_interaction for gifs.
TENOR_API_KEY = os.getenv("TENOR_API_KEY")

# The beginning of API url.
# Not needed if API_REQUIRED = False.
# [example] https://localhost:8080/api/
PATH_TO_API: str = os.getenv("PATH_TO_API") # type: ignore

# Main Guild of the bot.
# Is required for logger to send webhooks without provided guild id.
BASE_GUILD_ID = 1296417944934285313
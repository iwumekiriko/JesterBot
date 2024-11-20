import os
from dotenv import load_dotenv

load_dotenv()


APP_NAME = "JesterBot"
COGS_PATH = "src/cogs"
DEBUG = True


TOKEN = os.getenv("TOKEN")
TENOR_API_KEY = os.getenv("API_KEY")


LOG_WEBHOOK: str = os.getenv("LOG_WEBHOOK") # type: ignore


SUPPORT_ROLE_ID = 1303666566633754675
MODERATOR_ROLE_ID = 1303666632635322388
DEVELOPER_ROLE_ID = 1303666606576242698
OWNER_ID = 567303956448018456
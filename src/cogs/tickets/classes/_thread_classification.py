from enum import IntEnum

from src._config import (
    SUPPORT_ROLE_ID, MODERATOR_ROLE_ID, DEVELOPER_ROLE_ID)


class ThreadClassification(IntEnum):
    SUPPORT = SUPPORT_ROLE_ID
    MODERATOR = MODERATOR_ROLE_ID
    DEVELOPER = DEVELOPER_ROLE_ID
    
    

    
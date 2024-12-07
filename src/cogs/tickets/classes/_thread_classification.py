from enum import Enum


class ThreadClassification(Enum):
    SUPPORT = 1
    MODERATOR = 2
    DEVELOPER = 3

    def get_role_id(self, guild_id: int) -> int:
        from src.config import cfg

        role_key = {
            ThreadClassification.SUPPORT: "support_role_id",
            ThreadClassification.MODERATOR: "moderator_role_id",
            ThreadClassification.DEVELOPER: "developer_role_id",
        }[self]
        return getattr(cfg.config[guild_id]["Roles"], role_key)

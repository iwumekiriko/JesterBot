from dataclasses import dataclass

from .base_config import BaseConfig


@dataclass
class RolesConfig(BaseConfig):
    support_role_id: int | None = None
    moderator_role_id: int | None = None
    developer_role_id: int | None = None
    
    def to_dict(self) -> dict:
        return {
            "guildId": self.guild_id,
            "supportRoleId": self.support_role_id,
            "moderatorRoleId": self.moderator_role_id,
            "developerRoleId": self.developer_role_id
        }
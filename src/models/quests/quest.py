from datetime import datetime
from enum import Enum
from dataclasses import dataclass
from typing import Optional

from ..guild import Guild
from ..user import User
from .quest_reward_types import QuestRewardTypes
from .quest_task_types import QuestTaskTypes
from .quest_types import QuestTypes
from .quests_config import QuestsConfig


@dataclass
class Quest:
    id: int
    guild_id: int
    guild: Guild
    user_id: int
    user: User
    type: QuestTypes
    task_type: QuestTaskTypes
    channel_id: Optional[int]
    required: int
    progress: int
    reward_type: QuestRewardTypes
    reward_amount: int
    valid: bool
    assigned_at: datetime
    completed_at: Optional[datetime]
    completable_until: datetime
    is_completed: bool
    accepted_by_user: bool

    @property
    def thumbnail(self) -> Optional[str]:
        return QuestsConfig.assets.get(self.task_type, {}).get("thumbnail")

    @property
    def embed_color(self) -> Optional[str]:
        return QuestsConfig.assets.get(self.task_type, {}).get("embed_color")

    @property
    def description(self) -> str:
        return QuestsConfig.get_desc(
            self.task_type,
            self.id,
        )

    @property
    def title(self) -> str:
        return QuestsConfig.get_title(
            self.task_type,
            self.id
        )
    
    @property
    def task_desc(self) -> str:
        return QuestsConfig.get_task_desc(
            self.task_type,
            self.required,
            self.progress or 0,
            self.channel_id or 0
        )

    @property
    def reward_string(self) -> str:
        return QuestsConfig.get_reward_string(
            self.reward_type,
            self.reward_amount,
            self.guild_id
        )

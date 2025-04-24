from typing import List, Optional

from src.api_client import APIClient
from src.config import cfg as config
from src._api_interaction import set_cfg
from src.models.config import QuestsConfig
from src.models.quests import Quest, QuestTypes, QuestRewardTypes, QuestTaskTypes
from src.utils.enums import Actions
from src.utils._mapping import json_camel_to_snake
from src.utils._time import string_to_datetime


async def set_quests_message(
    guild_id: int,
    quests_message_id: int
) -> None:
    cfg = QuestsConfig(
            guild_id=guild_id,
            quests_message_id=quests_message_id)
    config.set_(cfg)
    await set_cfg(cfg)


async def get_user_quests(guild_id: int, user_id: int) -> List[Quest]:
    endpoint = f"Quests/{guild_id}/{user_id}"
    async with APIClient() as client:
        return _process_quests(await client.get(endpoint))


async def get_quest_board_img(guild_id: int) -> str:
    endpoint = f"Quests/{guild_id}/board-img"
    async with APIClient() as client:
        return (await client.get(endpoint))["img"]


async def get_available_now_guild_quests(guild_id: int, user_id: int, type: QuestTypes) -> List[Quest]:
    endpoint = f"Quests/{guild_id}/available/{user_id}/{type.value}"
    async with APIClient() as client:
        return _process_quests(await client.get(endpoint))


def _process_quests(response: List) -> List[Quest]:
    quests = []

    for quest in response:
        quest["type"] = QuestTypes(str(quest["type"]))
        quest["rewardType"] = QuestRewardTypes(str(quest["rewardType"]))
        quest["taskType"] = QuestTaskTypes(str(quest["taskType"]))
        quest["completableUntil"] = string_to_datetime(quest["completableUntil"])
        quest["completedAt"] = string_to_datetime(quest["completedAt"])
        quests.append(Quest(**json_camel_to_snake(quest)))

    return quests


async def accept_quest(guild_id: int, user_id: int, quest_id: int) -> None:
    endpoint = f"Quests/{guild_id}/accept/{user_id}/{quest_id}"
    async with APIClient() as client:
        await client.post(endpoint)


async def handle_quest_template(
    action: Actions,
    guild_id: int,
    time_type: QuestTypes,
    task_type: QuestTaskTypes,
    required: int,
    reward_type: QuestRewardTypes,
    reward_amount: int,
    weight: float,
    channel_id: Optional[int]
) -> None:
    endpoint = f"Quests/{guild_id}/templates"
    body = {
        "GuildId": guild_id,
        "Type": int(time_type),
        "TaskType": int(task_type),
        "Required": required,
        "RewardType": int(reward_type),
        "RewardAmount": reward_amount,
        "Weight": weight,
        "ChannelId": channel_id
    }
    async with APIClient() as client:
        match action:

            case Actions.ADD:
                 await client.post(endpoint, body=body)

            case Actions.REMOVE:
                await client.delete(endpoint, body=body)


async def update_quests() -> None:
    endpoint = f"Quests/update"
    async with APIClient() as client:
        await client.post(endpoint)

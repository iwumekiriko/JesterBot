from typing import Optional

from src.utils._mapping import json_camel_to_snake
from src.models import Duet
from src.api_client import APIClient


async def become_duet(guild_id: int, proposer_id: int, duo_id: int) -> None:
    endpoint = f"Duets/{guild_id}/{proposer_id}/{duo_id}"
    async with APIClient() as client:
        await client.post(endpoint)


async def become_solo(guild_id: int, user_id: int) -> None:
    endpoint = f"Duets/{guild_id}/{user_id}"
    async with APIClient() as client:
        await client.delete(endpoint)


async def get_duet(guild_id: int, user_id: int) -> Optional[Duet]:
    endpoint = f"Duets/{guild_id}/{user_id}"
    async with APIClient() as client:
        response = await client.get(endpoint)
        if (not response): return None
        return Duet(**json_camel_to_snake(response))

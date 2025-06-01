from typing import List
import aiohttp
import random
import json

from src.models.interactions import InteractionsAsset

from ._interactions_choice import InteractionActions, InteractionTypes
from src.utils._exceptions import CustomException
from src.api_client import APIClient


async def get_gif(
    guild_id: int,
    action_value: int,
    type_type: int
) -> str:
    endpoint = f"Interactions/{guild_id}/{action_value}/{type_type}"
    async with APIClient() as client:
        return (await client.get(endpoint))['assetUrl']


async def upload_gifs(guild_id: int, gifs: List[InteractionsAsset]) -> None:
    endpoint = f"Interactions/{guild_id}/upload"
    async with APIClient() as client:
        await client.put(
            endpoint,
            body=[gif.to_dict() for gif in gifs] # type: ignore
        )
import aiohttp
from typing import Optional

from src.settings import PATH_TO_API
from src.utils._exceptions import CustomException
from src.utils._mapping import json_camel_to_snake
from src.models import Duet


async def become_duet(guild_id: int, proposer_id: int, duo_id: int) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            PATH_TO_API + f"Duets/{guild_id}/{proposer_id}/{duo_id}", ssl=False
        ) as response:
            if response.status != 200:
                error_message = await response.text()
                raise CustomException(f"Duets API [duo] is not responding. "
                                    f"Status code: {response.status}. Error: {error_message}")                             


async def become_solo(guild_id: int, user_id: int) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.delete(
            PATH_TO_API + f"Duets/{guild_id}/{user_id}", ssl=False
        ) as response:
            if response.status != 200:
                error_message = await response.text()
                raise CustomException(f"Duets API [solo] is not responding. "
                                    f"Status code: {response.status}. Error: {error_message}")


async def get_duet(guild_id: int, user_id: int) -> Optional[Duet]:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            PATH_TO_API + f"Duets/{guild_id}/{user_id}", ssl=False
        ) as response:
            if response.status == 200:
                json_data = await response.json()
                return Duet(**json_camel_to_snake(json_data))
            if response.status == 204:
                return None
            else:
                error_message = await response.text()
                raise CustomException(f"Duets API [get] is not responding. "
                                    f"Status code: {response.status}. Error: {error_message}")
                
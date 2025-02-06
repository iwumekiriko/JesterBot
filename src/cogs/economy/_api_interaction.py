import aiohttp

from src.settings import PATH_TO_API
from src.utils._exceptions import CustomException
from src.models import Member
from src.utils._mapping import json_camel_to_snake
from src.utils._exceptions import NotEnoughMoneyException


async def coins_(guild_id: int, user_id: int, amount: int) -> Member:
    async with aiohttp.ClientSession() as session:
        async with session.put(
            PATH_TO_API + f"Members/{guild_id}/{user_id}/coins?amount={amount}", ssl=False
        ) as response:
            if response.status == 200:
                json_data = await response.json()
                return Member(**json_camel_to_snake(json_data))
            if response.status == 400:
                raise NotEnoughMoneyException
            else:
                error_message = await response.text()
                raise CustomException(f"Members API [coins] is not responding. "
                                    f"Status code: {response.status}. Error: {error_message}")
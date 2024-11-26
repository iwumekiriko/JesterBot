import aiohttp
from disnake import Member as dsMember

from src._config import PATH_TO_API
from src.utils._exceptions import BaseException
from src.utils._mapping import json_camel_to_snake
from src.models import Member as mdlMember


async def add_experience(member: dsMember) -> mdlMember:
    user_id = member.id
    guild_id = member.guild.id

    async with aiohttp.ClientSession() as session:
        async with session.put(
            PATH_TO_API + f"Members/Experience/{user_id}/{guild_id}/update?type=message", ssl=False
        ) as response:
            if response.status == 200:
                json_data = await response.json()
                return mdlMember(**json_camel_to_snake(json_data))
            else:
                error_message = await response.text()
                raise BaseException("Members API [Experience] is not responding. "
                                    f"Status code: {response.status}. Error: {error_message}")


async def add_coins(member: mdlMember) -> None:
    user_id = member.user_id
    guild_id = member.guild_id

    async with aiohttp.ClientSession() as session:
        async with session.put(
            PATH_TO_API + f"Members/Experience/{user_id}/{guild_id}/update?type=newLevel", ssl=False
        ) as response:
            if not response.status == 200:
                error_message = await response.text()
                raise BaseException("Members API [Experience] is not responding. "
                                    f"Status code: {response.status}. Error: {error_message}")
                
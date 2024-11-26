import aiohttp
import json

from src.logger import get_logger
from src.models import Member
from src._config import PATH_TO_API
from src.utils._mapping import json_camel_to_snake


logger = get_logger()


async def get_member(user_id: int, guild_id: int) -> Member:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            PATH_TO_API + f"Members/Get?userId={user_id}&guildId={guild_id}", ssl=False
        ) as response:
            if response.status == 200:
                json_data = await response.json()
                return Member(**json_camel_to_snake(json_data))
            else:
                error_message = await response.text()
                raise BaseException("Members API [Get] is not responding. "
                                    f"Status code: {response.status}. Error: {error_message}")
            

async def member_joined(member: Member) -> None:
    member.is_active = True
    member_data = json.dumps(member.to_on_guild())
    headers = {'Content-Type': 'application/json'}

    async with aiohttp.ClientSession() as session:
        async with session.put(
            PATH_TO_API + "Members/OnGuild",
            data=member_data, ssl=False, headers=headers
        ) as response:
            if not response.status == 200:
                error_message = await response.text()
                raise BaseException("Members API [OnGuild] is not responding. "
                                    f"Status code: {response.status}. Error: {error_message}")
            

async def member_left(member: Member) -> None:
    member.is_active = False
    member_data = json.dumps(member.to_on_guild())
    headers = {'Content-Type': 'application/json'}

    async with aiohttp.ClientSession() as session:
        async with session.put(
            PATH_TO_API + "Members/OnGuild",
            data=member_data, ssl=False, headers=headers
        ) as response:
            if not response.status == 200:
                error_message = await response.text()
                raise BaseException("Members API [OnGuild] is not responding. "
                                    f"Status code: {response.status}. Error: {error_message}")
import aiohttp
import json

from disnake import Member as dsMember

from src.logger import get_logger
from src.models import Member as mdlMember
from src.settings import PATH_TO_API
from src.utils._mapping import json_camel_to_snake
from src.utils._exceptions import CustomException


logger = get_logger()


async def get_member(guild_id: int, user_id: int) -> mdlMember:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            PATH_TO_API + f"Members/{guild_id}/{user_id}", ssl=False
        ) as response:
            if response.status == 200:
                json_data = await response.json()
                return mdlMember(**json_camel_to_snake(json_data))
            else:
                error_message = await response.text()
                raise CustomException("Members API [Get] is not responding. "
                                    f"Status code: {response.status}. Error: {error_message}")
            

async def member_joined(guild_id: int, user_id: int) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.put(
            PATH_TO_API + f"Members/{guild_id}/{user_id}/join", ssl=False
        ) as response:
            if not response.status == 200:
                error_message = await response.text()
                raise CustomException("Members API [OnGuild] is not responding. "
                                    f"Status code: {response.status}. Error: {error_message}")
            

async def member_left(guild_id: int, user_id: int) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.put(
            PATH_TO_API + f"Members/{guild_id}/{user_id}/leave", ssl=False
        ) as response:
            if not response.status == 200:
                error_message = await response.text()
                raise CustomException("Members API [OnGuild] is not responding. "
                                    f"Status code: {response.status}. Error: {error_message}")
            

async def update_member(member: mdlMember) -> None:
    guild_id = member.guild_id
    user_id = member.user_id
    member_data = json.dumps(member.to_update())
    headers = {'Content-Type': 'application/json'}

    async with aiohttp.ClientSession() as session:
        async with session.put(
            PATH_TO_API + f"Members/{guild_id}/{user_id}/update",
            data=member_data, ssl=False, headers=headers
        ) as response:
            if not response.status == 200:
                error_message = await response.text()
                raise CustomException("Members API [Update] is not responding. "
                                    f"Status code: {response.status}. Error: {error_message}")
            

async def add_message_experience(member: dsMember) -> mdlMember:
    guild_id = member.guild.id
    user_id = member.id

    async with aiohttp.ClientSession() as session:
        async with session.put(
            PATH_TO_API + f"Members/{guild_id}/{user_id}/message", ssl=False
        ) as response:
            if response.status == 200:
                json_data = await response.json()
                return mdlMember(**json_camel_to_snake(json_data))
            else:
                error_message = await response.text()
                raise CustomException("Members API [Experience] is not responding. "
                                    f"Status code: {response.status}. Error: {error_message}")


async def add_voice_time(member: dsMember, seconds: int) -> mdlMember:
    guild_id = member.guild.id
    user_id = member.id

    async with aiohttp.ClientSession() as session:
        async with session.put(
            PATH_TO_API + f"Members/{guild_id}/{user_id}/voice?seconds={seconds}", ssl=False
        ) as response:
            if response.status == 200:
                json_data = await response.json()
                return mdlMember(**json_camel_to_snake(json_data))
            else:
                error_message = await response.text()
                raise CustomException("Members API [VoiceTime] is not responding. "
                                    f"Status code: {response.status}. Error: {error_message}")
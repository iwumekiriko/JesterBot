import aiohttp
from disnake import Member as dsMember

from src.settings import PATH_TO_API
from src.utils._exceptions import CustomException
from src.utils._mapping import json_camel_to_snake
from src.models import Member as mdlMember


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
                
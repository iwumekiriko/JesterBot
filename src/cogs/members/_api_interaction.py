import aiohttp
import json

from disnake import Member as dsMember

from src.logger import get_logger
from src.models import Member as mdlMember
from src.settings import API_PATH
from src.utils._mapping import json_camel_to_snake
from src.utils._exceptions import CustomException
from src.api_client import APIClient


logger = get_logger()


async def get_member(guild_id: int, user_id: int) -> mdlMember:
    endpoint = f"Members/{guild_id}/{user_id}"
    async with APIClient() as client:
        response = await client.get(endpoint)
        return mdlMember(**json_camel_to_snake(response)) # type: ignore
            

async def member_joined(guild_id: int, user_id: int) -> None:
    endpoint = f"Members/{guild_id}/{user_id}/join"
    async with APIClient() as client:
        await client.put(endpoint)
            

async def member_left(guild_id: int, user_id: int) -> None:
    endpoint = f"Members/{guild_id}/{user_id}/leave"
    async with APIClient() as client:
        await client.put(endpoint)
            

async def update_member(member: mdlMember) -> None:
    guild_id = member.guild_id
    user_id = member.user_id
    member_data = member.to_update()
    endpoint = f"Members/{guild_id}/{user_id}/update"
    async with APIClient() as client:
        await client.put(
            endpoint,
            body=member_data
        )


async def add_message_experience(member: dsMember) -> mdlMember:
    guild_id = member.guild.id
    user_id = member.id
    endpoint = f"Members/{guild_id}/{user_id}/message"
    async with APIClient() as client:
        response = await client.put(endpoint)
        return mdlMember(**json_camel_to_snake(response)) # type: ignore


async def add_voice_time(member: dsMember, seconds: int) -> mdlMember:
    guild_id = member.guild.id
    user_id = member.id
    endpoint = f"Members/{guild_id}/{user_id}/voice"
    query_params = {"seconds": seconds}
    async with APIClient() as client:
        response = await client.put(
            endpoint,
            query_params=query_params
        )
        return mdlMember(**json_camel_to_snake(response)) # type: ignore

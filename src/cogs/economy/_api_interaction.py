from src.models import Member
from src.utils._mapping import json_camel_to_snake
from src.api_client import APIClient


async def update_member_coins(guild_id: int, user_id: int, amount: int) -> Member:
    endpoint = f"Members/{guild_id}/{user_id}/coins"
    query_params = {"amount": amount}
    async with APIClient() as client:
        response = await client.put(
            endpoint,
            query_params=query_params
        )
        return Member(**json_camel_to_snake(response))
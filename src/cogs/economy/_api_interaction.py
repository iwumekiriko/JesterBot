from typing import Optional

from src.models import Member
from src.utils._mapping import json_camel_to_snake
from src.api_client import APIClient
from src.utils.enums import Currency


async def make_transaction(
    currency: Currency,
    guild_id: int,
    payer_id: int,
    amount: int,
    recipient_id: Optional[int] = None
) -> Member:
    if not recipient_id:
        from src.bot import bot
        recipient_id = bot.user.id

    endpoint = f"Economy/{guild_id}/transactions/{currency.name.lower()}/{payer_id}/{recipient_id}"
    query_params = {"amount": amount}

    async with APIClient() as client:
        response = await client.post(
            endpoint,
            query_params=query_params
        )
        return Member(**json_camel_to_snake(response))


async def proceed_coins_reward(
    guild_id: int,
    recipient_id: int,
    amount: int
) -> Member:
    from src.bot import bot
    payer_id = bot.user.id

    endpoint = f"Economy/{guild_id}/transactions/{Currency.COINS.name.lower()}/{payer_id}/{recipient_id}"
    query_params = {"amount": amount}

    async with APIClient() as client:
        response = await client.post(
            endpoint,
            query_params=query_params
        )
        return Member(**json_camel_to_snake(response))
from typing import Dict, List

from src._api_interaction import set_cfg
from src.config import cfg as config
from src.models.config import ShopConfig
from src.models.shop import ShopRole, ShopKey, ShopRoleTries
from src.api_client import APIClient
from src.utils._mapping import json_camel_to_snake
from src.models.lootboxes import LootboxTypes
from src.utils.enums import Actions


async def set_shop_message(
    guild_id: int,
    shop_message_id: int
) -> None:
    cfg = ShopConfig(
            guild_id=guild_id,
            shop_message_id=shop_message_id)
    config.set_(cfg)
    await set_cfg(cfg)


async def get_user_shop_roles(guild_id: int, user_id: int) -> List[ShopRole]:
    endpoint = f"Shop/{guild_id}/roles/{user_id}"
    async with APIClient() as client:
        response = await client.get(endpoint)
        return [ShopRole(**json_camel_to_snake(role)) for role in response]


async def get_shop_keys(guild_id: int, user_id: int) -> List[ShopKey]:
    endpoint = f"Shop/{guild_id}/keys"
    async with APIClient() as client:
        response = await client.get(endpoint)
        [item.update({"lootboxType": LootboxTypes(item["lootboxType"])}) for item in response]
        return [ShopKey(**json_camel_to_snake(key)) for key in response]


async def handle_shop_role(
    guild_id: int,
    action: Actions,
    guild_role_id: int,
    price: int,
    exclusive: bool
) -> None:
    endpoint = f"Shop/{guild_id}/roles/{guild_role_id}"
    query_params = { "price": price, "exclusive": str(exclusive) }
    async with APIClient() as client:
        match action:

            case Actions.ADD:
                 await client.post(endpoint, query_params=query_params)

            case Actions.REMOVE:
                await client.delete(endpoint)


async def handle_shop_key(
    guild_id: int,
    action: Actions,
    lootbox_type: LootboxTypes,
    exclusive: bool
) -> None:
    endpoint = f"Shop/{guild_id}/keys/{lootbox_type.value}"
    query_params = { "exclusive": str(exclusive) }
    async with APIClient() as client:
        match action:

            case Actions.ADD:
                 await client.post(endpoint, query_params=query_params)

            case Actions.REMOVE:
                await client.delete(endpoint)


async def get_shop_role_tries(
    guild_id: int,
    user_id: int,
    guild_role_id: int
) -> ShopRoleTries:
    endpoint = f"Shop/{guild_id}/roles/{user_id}/{guild_role_id}/try"
    async with APIClient() as client:
        response = await client.get(endpoint)
        return ShopRoleTries(**json_camel_to_snake(response))


async def try_shop_role(
    guild_id: int,
    user_id: int,
    guild_role_id: int
) -> None:
    endpoint = f"Shop/{guild_id}/roles/{user_id}/{guild_role_id}/try"
    async with APIClient() as client:
        await client.put(endpoint)


async def reset_shop_roles_tries(
    guild_id: int
) -> List[Dict[str, int]]:
    endpoint = f"Shop/{guild_id}/roles/tries/reset"
    async with APIClient() as client:
        return await client.post(endpoint)
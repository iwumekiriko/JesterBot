from typing import Dict, List, Type, Optional

from src.utils._mapping import json_camel_to_snake
from src.api_client import APIClient
from src.models.inventory_items import (
    Item, ExpBooster, LootboxKey, Coin, Role
)
from src.models.lootboxes import (
    LootboxUserData, BaseData, LootboxRole,
    RolesData, BackgroundsData, LootboxTypes
)
from src.utils.enums import Actions


item_endpoints: Dict[type[Item], str] = {
    ExpBooster: "exp-boosters",
    LootboxKey: "lootbox-keys",
    Role: "roles",
    Coin: "coins"
}


async def add_item_to_inventory(
    guild_id: int, user_id: int,
    item_type: Type[Item], *,
    body: Optional[Dict] = None
) -> Item:
    endpoint = f"Inventory/{guild_id}/{user_id}/{item_endpoints[item_type]}/add"
    async with APIClient() as client:
        response = await client.post(
            endpoint,
            body=body
        )
        return item_type(**json_camel_to_snake(_process_list(response, item_type)))


def _process_list(
    data: dict,
    item_type: Type[Item]
) -> dict:
    item_data = data["item"]
    if item_type is LootboxKey:
        item_data["type"] = LootboxTypes(item_data["type"])
    item_data["quantity"] = data["quantity"]

    return item_data


async def keys_count(guild_id: int, user_id: int, type: LootboxTypes) -> int:
    endpoint = f"Inventory/{guild_id}/{user_id}/lootbox-keys/{type.value}"
    async with APIClient() as client:
        return await client.get(endpoint)


async def manage_keys(guild_id: int, user_id: int, type: LootboxTypes, count: int) -> None:
    endpoint = f"Inventory/{guild_id}/{user_id}/lootbox-keys/{type.value}?count={count}"
    async with APIClient() as client:
        await client.put(endpoint)


async def owns_role(guild_id: int, user_id: int, guild_role_id: int) -> bool:
    endpoint = f"Inventory/{guild_id}/{user_id}/roles/{guild_role_id}"
    async with APIClient() as client:
        return await client.get(endpoint)


async def get_lootbox_data(guild_id: int, user_id: int, type: LootboxTypes) -> LootboxUserData:
    endpoint = f"Lootboxes/{guild_id}/data/{user_id}/{type.value}"
    async with APIClient() as client:
        lootbox_data = await client.get(endpoint)
        lootbox_data = _process_type(lootbox_data)
        lootbox_data["data"] = _create_data_from_dict(lootbox_data["lootboxType"], lootbox_data["data"])
        return LootboxUserData(**json_camel_to_snake(lootbox_data))


async def save_lootbox_data(data: LootboxUserData) -> None:
    endpoint = f"Lootboxes/{data.guild_id}/data/{data.user_id}/{data.lootbox_type.value}"
    async with APIClient() as client:
        await client.post(
            endpoint=endpoint,
            body=data.to_dict()
        )


async def get_lootbox_roles(guild_id: int, lootbox_type: LootboxTypes) -> List[LootboxRole]:
    endpoint = f"Lootboxes/{guild_id}/roles/{lootbox_type.value}"
    async with APIClient() as client:
        response = await client.get(endpoint)
        return [LootboxRole(**json_camel_to_snake(role)) for role in response]


async def get_user_lootbox_roles(guild_id: int, lootbox_type: LootboxTypes, user_id: int) -> List[LootboxRole]:
    endpoint = f"Lootboxes/{guild_id}/roles/{lootbox_type.value}/{user_id}"
    async with APIClient() as client:
        response = await client.get(endpoint)
        return [LootboxRole(**json_camel_to_snake(role)) for role in response]


async def handle_lootbox_role(
    guild_id: int,
    lootbox_type: LootboxTypes,
    guild_role_id: int,
    action: Actions,
    exclusive: bool
) -> None:
    endpoint = f"Lootboxes/{guild_id}/roles/{lootbox_type.value}/{guild_role_id}"
    query_params = { "exclusive": str(exclusive) }
    async with APIClient() as client:
        match action:

            case Actions.ADD:
                 await client.post(endpoint, query_params=query_params)

            case Actions.REMOVE:
                await client.delete(endpoint)


def _process_type(data: Dict) -> Dict:
    data["lootboxType"] = LootboxTypes(data["lootboxType"])
    return data


def _create_data_from_dict(data_type: LootboxTypes, data_dict: dict) -> BaseData:
    match (data_type):

        case LootboxTypes.ROLES_LOOTBOX:
            return RolesData(
                total_attempts=data_dict.get("totalAttempts", 0),
                roles_attempts=data_dict.get("rolesAttempts", 0),
                roles_got=data_dict.get("rolesGot", 0)
            )

        case LootboxTypes.BACKGROUNDS_LOOTBOX:
            return BackgroundsData(
                total_attempts=data_dict.get("totalAttempts", 0),
                backgrounds_attempts=data_dict.get("backgroundsAttempts", 0),
                backgrounds_got=data_dict.get("backgroundsGot", 0)
            )

        case _:
            return BaseData(total_attempts=data_dict.get("totalAttempts", 0))

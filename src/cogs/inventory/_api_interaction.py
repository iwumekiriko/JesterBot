from typing import List, Optional, Dict, Any, Union

from src.logger import get_logger
from src.api_client import APIClient

from src.utils._mapping import json_camel_to_snake
from src.utils._converters import user_avatar

from src.models.inventory import Inventory
from src.models.inventory_items import (
    Role,
    ExpBooster, ActiveExpBooster,
    LootboxKey,
    Pack
)
from src.models.lootboxes import LootboxTypes
from src.models import Guild, User


logger = get_logger()


async def get_inventory(guild_id: int, user_id: int) -> Inventory:
    endpoint = f"Inventory/{guild_id}/{user_id}"
    async with APIClient() as client:
        response: Dict[str, Any] = await client.get(endpoint)
        
        inv_id = response.get("inventory_id", 0)
        
        guild = response.get("guild", Guild(id=guild_id)) 
        user = response.get("user", User(id=user_id))

        roles = _process_dict(response.get("roles"), Role)
        exp_boosters = _process_dict(response.get("expBoosters"), ExpBooster, sort_key=('value', 'duration'))
        lootbox_keys = _process_dict(response.get("lootboxKeys"), LootboxKey, LootboxTypes)
        packs = [Pack(
            guild=None,
            guild_id=guild_id,
            quantity=pack["amount"],
            id=pack["id"],
            name=pack["name"]
        ) for pack in response.get("packs", {}) if pack["amount"] > 0]

        return Inventory(
            inventory_id=inv_id,
            guild_id=guild_id,
            guild=guild,
            user_id=user_id,
            user=user,
            roles=roles,
            exp_boosters=exp_boosters,
            lootbox_keys=lootbox_keys,
            packs=packs
        )


def _process_dict(
    data: Optional[dict],
    data_class,
    type_enum=None,
    sort_key: Optional[Union[str, tuple]] = None
) -> Optional[List]:
    if not data:
        return None
    result = []
    for item_data in data.values():
        if type_enum:
            item_data["type"] = type_enum(item_data["type"])
        result.append(data_class(**json_camel_to_snake(item_data)))

    if sort_key and result:
        key_func = (lambda x: getattr(x, sort_key)) if isinstance(sort_key, str) else (
                    lambda x: tuple(getattr(x, attr) for attr in sort_key))
        result.sort(key=key_func)

    return result


async def use_booster(
    guild_id: int,
    user_id: int,
    booster_value: int,
    booster_duration: int
) -> None:
    endpoint = f"Inventory/{guild_id}/{user_id}/exp-boosters/use"
    body = { "value": booster_value, "duration": booster_duration, "quantity": 1 }
    async with APIClient() as client:
        await client.post(
            endpoint,
            body=body
        )
        logger.debug("Пользователь <@%d> использует буст", user_id,
                    extra={
                        "user_avatar": user_avatar(user_id),
                        "type": "else",
                        "guild_id": guild_id
                    })
        return None


async def reset_boosters(guild_id: int) -> List[int]:
    endpoint = f"Inventory/{guild_id}/exp-boosters/reset"
    async with APIClient() as client:
        return await client.post(endpoint)


async def cancel_booster(guild_id: int, user_id: int) -> None:
    endpoint = f"Inventory/{guild_id}/{user_id}/exp-boosters/cancel"
    async with APIClient() as client:
        await client.post(endpoint)
        logger.debug("Пользователь <@%d> отменяет буст", user_id,
                    extra={
                        "user_avatar": user_avatar(user_id),
                        "type": "else",
                        "guild_id": guild_id
                    })


async def get_active_booster(guild_id: int, user_id: int) -> Optional[ActiveExpBooster]:
    endpoint = f"Inventory/{guild_id}/{user_id}/exp-boosters/active"
    async with APIClient() as client:
        response = await client.get(endpoint)
        if not response:
            return None

        return ActiveExpBooster(**json_camel_to_snake(response), quantity=1)


async def get_member_roles(guild_id: int, user_id: int) -> List[Role]:
    endpoint = f"Inventory/{guild_id}/{user_id}/roles"
    async with APIClient() as client:
        response = await client.get(endpoint)
        return [Role(**json_camel_to_snake(role)) for role in response]

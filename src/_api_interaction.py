from typing import TypeVar

from src.models.config.base_config import BaseConfig
from src.utils._mapping import json_camel_to_snake
from src.api_client import APIClient


T = TypeVar('T', bound='BaseConfig')


async def get_cfg(guild_id: int, cfg_type: type[T]) -> T:
    endpoint = f"Config/{cfg_type(0).short_name}/{guild_id}"
    async with APIClient() as client:
        response = await client.get(endpoint)
        return cfg_type(**json_camel_to_snake(response))


async def set_cfg(cfg: T) -> None: # type: ignore
    data = cfg.to_dict()
    endpoint = f"Config/{cfg.short_name}"
    async with APIClient() as client:
        await client.put(endpoint, body=data)


async def send_log_to_api(log) -> None:
    endpoint = "Logs"

    async with APIClient() as client:
        await client.post(endpoint, body = log.to_dict())

import json
import aiohttp
from typing import TypeVar

from src.models.config.base_config import BaseConfig
from src.utils._mapping import json_camel_to_snake
from src.settings import PATH_TO_API


T = TypeVar('T', bound='BaseConfig')


async def get_cfg(guild_id: int, cfg_type: type[T]) -> T:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            PATH_TO_API + f"Config/{cfg_type.__name__}/Get/{guild_id}", ssl=False
        ) as response:
            if response.status == 200:
                json_data = await response.json()
                return cfg_type(**json_camel_to_snake(json_data))
            else:
                error_message = await response.text()
                raise BaseException(f"Config API [{cfg_type.short_name}] is not responding. "
                                    f"Status code: {response.status}. Error: {error_message}")


async def set_cfg(cfg: T) -> None:
    guild_id = cfg.guild_id

    data = json.dumps(cfg.to_dict())
    headers = {'Content-Type': 'application/json'}

    async with aiohttp.ClientSession() as session:
        async with session.put(
            PATH_TO_API + f"Config/{cfg.__class__.__name__}/Set/{guild_id}",
                ssl=False, data=data, headers=headers
        ) as response:
            if not response.status == 200:
                error_message = await response.text()
                raise BaseException(f"Config API [{cfg.short_name}] is not responding. "
                                    f"Status code: {response.status}. Error: {error_message}")

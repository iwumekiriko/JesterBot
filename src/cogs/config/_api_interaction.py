from src.models.config.base_config import BaseConfig
from src._api_interaction import set_cfg
from src.config import cfg as config


async def set_local_cfg(data: dict, type: type[BaseConfig]) -> None:
    cfg = type(**data)
    config.set_(cfg)
    await set_cfg(cfg)
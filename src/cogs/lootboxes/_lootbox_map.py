from enum import Enum
from typing import Any, ClassVar, Dict, List, Type

from src.localization import get_localizator
from .types import BaseLootbox, RolesLootbox, BackgroundsLootbox
from src.models.lootboxes.lootbox_types import LootboxTypes


_ = get_localizator("lootboxes")


class LootboxMap(str, Enum):
    ROLES_LOOTBOX = "roles"
    BACKGROUNDS_LOOTBOX = "backgrounds"

    @classmethod
    def _type_mapping(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "roles": {
                'class': RolesLootbox,
                'lootbox_type': LootboxTypes.ROLES_LOOTBOX,
                'has_roles': True
            },
            "backgrounds": {
                'class': BackgroundsLootbox,
                'lootbox_type': LootboxTypes.BACKGROUNDS_LOOTBOX,
                'has_roles': False
            }
        }

    @classmethod
    def to_class(cls, type_value: str):
        return cls._type_mapping()[type_value]['class']

    def translated(self) -> str:
        return _(f'lootboxes-{self.value}_lootbox_name')

    @classmethod
    def to_type(cls, type_value: str) -> LootboxTypes:
        return cls._type_mapping()[type_value]['lootbox_type']

    @classmethod
    def from_type(cls, lootbox_type: Type[BaseLootbox]) -> 'LootboxMap':
        for lb in cls:
            if cls._type_mapping()[lb.value]['class'] is lootbox_type:
                return lb
        raise ValueError(f"Unknown lootbox type: {lootbox_type}")

    @classmethod
    def is_active(cls, lootbox_type: Type[BaseLootbox], guild_id: int) -> bool:
        lb_map = cls.from_type(lootbox_type)
        return lb_map in cls.actives(guild_id)

    @classmethod
    def actives(cls, guild_id: int) -> list['LootboxMap']:
        from src.config import cfg
        lc = cfg.lootboxes_cfg(guild_id)

        values = ([value.strip() for value in lc.active_lootboxes.split("|")]
                   if lc.active_lootboxes else [])
        return [LootboxMap(value) for value in values if value in cls.__members__.values()]

    @classmethod
    def w_roles(cls, guild_id: int) -> list['LootboxMap']:
        lootboxes_with_roles = [
            lb for lb in cls 
            if cls._type_mapping()[lb.value]['has_roles']
        ]
        return [
            lb for lb in lootboxes_with_roles 
            if cls.is_active(cls._type_mapping()[lb.value]['class'], guild_id)
        ]

    @classmethod
    def values(cls) -> str:
        return " | ".join(lb.value for lb in cls)

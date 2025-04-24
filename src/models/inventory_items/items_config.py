from typing import Dict

from src.localization import get_localizator

_ = get_localizator("items-config")

class ItemsConfig:
    descriptions: Dict[str, str] = {
        "ExpBooster": "items-config-exp_booster_desc",
        "LootboxKey": "items-config-lootbox_key_desc",
        "Role": "items-config-role_desc",
        "Coin": "items-config-coin_desc"
    }
    assets: Dict[str, Dict[str, str]] = {
        "ExpBooster": {
            "lootbox_gif": "https://i.pinimg.com/originals/d9/b2/9f/d9b29fdd541404f5df42c52362dca5bf.gif",
            "thumbnail": "https://i.imgur.com/xKICzua.jpeg",
            "embed_color": "0x123123"
        },
        "LootboxKey": {
            "lootbox_gif": "https://i.pinimg.com/originals/d9/b2/9f/d9b29fdd541404f5df42c52362dca5bf.gif",
            "thumbnail": "https://i.imgur.com/xKICzua.jpeg",
            "embed_color": "0x222222"
        },
        "Role": {
            "lootbox_gif": "https://i.pinimg.com/originals/d9/b2/9f/d9b29fdd541404f5df42c52362dca5bf.gif",
            "thumbnail": "https://i.imgur.com/xKICzua.jpeg",
            "embed_color": "0x333333"
        },
        "Coin": {
            "lootbox_gif": "https://i.pinimg.com/originals/d9/b2/9f/d9b29fdd541404f5df42c52362dca5bf.gif",
            "thumbnail": "https://i.imgur.com/xKICzua.jpeg",
            "embed_color": "0x111111"
        }
    }

    @staticmethod
    def get_translated_name(name: str) -> str:
        return _(f"items-config-{name}_name")

    @staticmethod
    def get_formatted_desc(item_type: str, **kwargs):
        return _(ItemsConfig.descriptions[item_type], **kwargs)
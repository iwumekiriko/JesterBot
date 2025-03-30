from enum import Enum


class CustomEvents(str, Enum):
    """
    Custom events for `bot.dispatch()`.
    """
    LOOTBOXES_ITEM_RECEIVED = 'lootboxes_item_received'
    GUILD_NITRO_BOOSTED = "guild_nitro_boosted"

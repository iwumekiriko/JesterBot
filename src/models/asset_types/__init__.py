from enum import Enum


class AssetTypes(Enum):
    GIF = 1
    IMAGE = 2


class GifTypes(Enum):
    INTERACTION_GIF = 1
    ITEM_GIF = 2


from src.cogs.interactions._interactions_choice import InteractionTypes, InteractionActions


__all__ = (
    'AssetTypes',
    'GifTypes',
    'InteractionTypes',
    'InteractionActions'
)
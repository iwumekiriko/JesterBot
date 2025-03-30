# from typing import Optional

# from .asset_types import *


# class Asset:
#     def __init__(
#         self,
#         id: int,
#         url: str,
#         type: AssetTypes,
#         gif_type: Optional[GifTypes] = None,
#         inter_action: Optional[InteractionActions] = None,
#         inter_type: Optional[InteractionTypes] = None
#     ) -> None:
#         self._id = id
#         self._url = url
#         self._type = type
#         self._gif_type = gif_type
#         self._inter_action = inter_action
#         self._inter_type = inter_type

#     @property
#     def id(self) -> int:
#         return self._id
    
#     @property
#     def url(self) -> str:
#         return self._url
    
#     @property
#     def type(self) -> AssetTypes:
#         return self._type
    
#     @property
#     def gif_type(self) -> Optional[GifTypes]:
#         return self._gif_type
    
#     @property
#     def inter_action(self) -> Optional[InteractionActions]:
#         return self._inter_action
    
#     @property
#     def inter_type(self) -> Optional[InteractionTypes]:
#         return self._inter_type

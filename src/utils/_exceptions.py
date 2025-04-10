from typing import Optional

from src.localization import get_localizator
from ._time import seconds_to_hms, make_discord_timestamp
from src.models.lootboxes import LootboxTypes


_ = get_localizator("exceptions")


class CustomException(Exception):
    """Base custom exception"""


class ModalTimeoutException(CustomException):
    def __init__(self, message: Optional[str] = None) -> None:
        if message is None:
            message = _("modal_timeout_exception")
        self.message = message
        super().__init__(self.message)


class LoggerException(CustomException):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class APIException(CustomException):
    def __init__(self, message: Optional[str] = None, **kwargs):
        if message is None:
            self.message = _("api_exception")
        super().__init__(self.message)


class NotEnoughMoneyException(APIException):
    def __init__(
        self,
        message: Optional[str] = None,
        **kwargs
    ) -> None:
        needed = kwargs.get("needed", -1)
        current = kwargs.get("current", -1)
        if message is None:
            message = _("not_enough_money_exception",
                         needed=needed, current=current)
        self.message = message
        super().__init__(self.message)


class BoosterAlreadyActiveException(APIException):
    def __init__(
        self,
        message: Optional[str] = None,
        **kwargs
    ) -> None:
        remaining: int = kwargs.get("remaining", 1)
        if message is None:
            message = _("booster_already_active_exception",
                        remaining=seconds_to_hms(remaining))
        self.message = message
        super().__init__(self.message)

    
class NoActiveBoosterException(APIException):
    def __init__(
        self,
        message: Optional[str] = None,
        **kwargs
    ) -> None:
        if message is None:
            message = _("no_active_booster_exception")
        self.message = message
        super().__init__(self.message)


class AlreadyOwnsRoleException(APIException):
    def __init__(
        self,
        message: Optional[str] = None,
        **kwargs
    ) -> None:
        guild_role_id = kwargs.get("guildRoleId", 0)
        
        if message is None:
            message = _("already_owns_role_exception",
                        guild_role_id=guild_role_id)
        self.message = message
        super().__init__(self.message)


class NotEnoughItemsException(APIException):
    def __init__(
        self,
        message: Optional[str] = None,
        **kwargs
    ) -> None:
        current = kwargs.get("current", -1)
        needed = kwargs.get("needed", -1)
        item_type: str = kwargs.get("itemType", "")

        if message is None:
            message = _("not_enough_items_exception",
                        current=current,
                        needed=needed,
                        item_type=_(item_type))
        self.message = message
        super().__init__(self.message)


class LootboxRoleAlreadyExistsException(APIException):
    def __init__(
        self,
        message: Optional[str] = None,
        **kwargs
    ) -> None:
        type = LootboxTypes(kwargs.get("type", 1))
        guild_role_id = kwargs.get("guildRoleId", 0)

        if message is None:
            message = _("lootbox_role_already_exists_exception",
                        type=type.translated, guild_role_id=guild_role_id)
        self.message = message
        super().__init__(self.message)


class LootboxRoleDoesNotExistException(APIException):
    def __init__(
        self,
        message: Optional[str] = None,
        **kwargs
    ) -> None:
        type = LootboxTypes(kwargs.get("type", 1))
        guild_role_id = kwargs.get("guildRoleId", 0)

        if message is None:
            message = _("lootbox_role_does_not_exist_exception",
                        type=type.translated, guild_role_id=guild_role_id)
        self.message = message
        super().__init__(self.message)


class ShopRoleAlreadyExistsException(APIException):
    def __init__(
        self,
        message: Optional[str] = None,
        **kwargs
    ) -> None:
        guild_role_id = kwargs.get("guildRoleId", 0)

        if message is None:
            message = _("shop_role_already_exists_exception",
                        guild_role_id=guild_role_id)
        self.message = message
        super().__init__(self.message)


class ShopRoleDoesNotExistException(APIException):
    def __init__(
        self,
        message: Optional[str] = None,
        **kwargs
    ) -> None:
        guild_role_id = kwargs.get("guildRoleId", 0)

        if message is None:
            message = _("shop_role_does_not_exist_exception",
                        guild_role_id=guild_role_id)
        self.message = message
        super().__init__(self.message)


class ShopKeyAlreadyExistsException(APIException):
    def __init__(
        self,
        message: Optional[str] = None,
        **kwargs
    ) -> None:
        type = LootboxTypes(kwargs.get("lootboxType", 1))

        if message is None:
            message = _("shop_key_already_exists_exception",
                        type=type.translated)
        self.message = message
        super().__init__(self.message)


class ShopKeyDoesNotExistException(APIException):
    def __init__(
        self,
        message: Optional[str] = None,
        **kwargs
    ) -> None:
        type = LootboxTypes(kwargs.get("lootboxType", 1))

        if message is None:
            message = _("shop_key_does_not_exist_exception",
                        type=type.translated)
        self.message = message
        super().__init__(self.message)


class AllShopTriesAreUsedException(APIException):
    def __init__(
        self,
        message: Optional[str] = None,
        **kwargs
    ) -> None:
        guild_role_id = kwargs.get("guildRoleId", 0)

        if message is None:
            message = _("all_shop_tries_are_used_exception",
                        guild_role_id=guild_role_id)
        self.message = message
        super().__init__(self.message)


class LastTryDidntEndException(APIException):
    def __init__(
        self,
        message: Optional[str] = None,
        **kwargs
    ) -> None:
        will_end_at = kwargs.get("willEndAt", 0)

        if message is None:
            message = _("last_try_didnt_end_exception",
                        will_end_at=make_discord_timestamp(will_end_at, 'R'))
        self.message = message
        super().__init__(self.message)
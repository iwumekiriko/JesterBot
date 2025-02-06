from typing import Optional

from src.localization import get_localizator


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


class NotEnoughMoneyException(CustomException):
    def __init__(self, message: Optional[str] = None) -> None:
        if message is None:
            message = _("not_enough_money_exception")
        self.message = message
        super().__init__(self.message)

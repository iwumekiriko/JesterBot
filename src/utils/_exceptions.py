from typing import Optional

from src.localization import get_localizator


_ = get_localizator()


class BaseException(Exception):
    """Base exception for handling one in bot on_error event"""


class ModalTimeoutException(BaseException):
    def __init__(self, message: Optional[str] = None) -> None:
        if message is None:
            message = _("modal_timeout_exception")
        self.message = message
        super().__init__(self.message)
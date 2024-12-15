from typing import Optional

from src.localization import get_localizator


_ = get_localizator()


class BaseException(Exception):
    """Base exception"""


class ModalTimeoutException(BaseException):
    def __init__(self, message: Optional[str] = None) -> None:
        if message is None:
            message = _("modal_timeout_exception")
        self.message = message
        super().__init__(self.message)


class LoggerException(BaseException):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
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


class LogWebhooksNotSetException(BaseException):
    def __init__(self, message: Optional[str] = None) -> None:
        if message is None:
            message = _("log_webhooks_not_set_exception")
        self.message = message
        super().__init__(self.message)
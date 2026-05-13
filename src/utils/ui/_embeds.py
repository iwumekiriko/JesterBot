import disnake

from src.localization import get_localizator
from src.customisation import (
    BASE_EMBED_COLOR,
    BASE_EXCEPTION_COLOR,
    BASE_SUCCESS_COLOR,
    BASE_WARNING_COLOR
)


_ = get_localizator("general.ui")


class BaseEmbed(disnake.Embed):
    def __init__(
        self, **kwargs
    ) -> None:
        """
        Args:
            title (`str`): Embed's title.
            description (`str`): Embed's description.
            color: (`int`): Embed's color. (base setted in src/customisation.py)
        """
        super().__init__(
            title = kwargs.get('title'),
            description = kwargs.get('description'),
            color = kwargs.get("color", BASE_EMBED_COLOR)
        )


class ExceptionEmbed(BaseEmbed):
    def __init__(
        self, error_msg: str
    ) -> None:
        """
        Args:
            error_msg (`str`): Embed's description.
        """
        if (act_len := len(error_msg)) > 3500:
            error_msg = error_msg[:3500] + "..."

        super().__init__(
            title=_("exception_title"),
            description=error_msg,
            color=BASE_EXCEPTION_COLOR
        )
        self.set_footer(text=f'{len(error_msg)}/{act_len}')


class WarningEmbed(BaseEmbed):
    def __init__(
        self, warning_msg: str
    ) -> None:
        """
        Args:
            warning_msg (`str`): Embed's description.
        """
        super().__init__(
            title = _("warning_title"),
            description = warning_msg,
            color = BASE_WARNING_COLOR
        )


class SuccessEmbed(BaseEmbed):
    def __init__(
        self, success_msg: str
    ) -> None:
        """
        Args:
            success_msg (`str`): Embed's description.
        """
        super().__init__(
            title=_("success_title"),
            description = success_msg,
            color = BASE_SUCCESS_COLOR
        )
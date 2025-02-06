import disnake

from src.localization import get_localizator


_ = get_localizator("ui")


class BaseEmbed(disnake.Embed):
    def __init__(
        self, **kwargs
    ) -> None:
        """
        Args:
            title (`str`): Embed's title.
            description (`str`): Embed's description.
            color: (`int`): Embed's color. (base - 0xddbef8)
        """
        super().__init__(
            title = kwargs.get('title'),
            description = kwargs.get('description'),
            color = 0xddbef8,
        )


class ExceptionEmbed(BaseEmbed):
    def __init__(
        self, error_msg: str
    ) -> None:
        if (act_len := len(error_msg)) > 3500:
            error_msg = error_msg[:3500] + "..."

        self.set_footer(text=f'{len(error_msg)}/{act_len}')
        super().__init__(
            title=_("exception_title"),
            description=error_msg,
            color=0xe74c3c
        )
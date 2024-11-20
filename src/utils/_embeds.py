import disnake

from src.localization import get_localizator


_ = get_localizator()


class BaseEmbed(disnake.Embed):
    def __init__(
        self, **kwargs
    ) -> None:
        """
        Attributes
        ---------
        title: :class:`str`
            Embed's title.
        description: :class:`str`
            Embed's description.
        color: :class:`int`
            Embed's color. (base - 0xddbef8)
        """
        super().__init__(
            title = kwargs.get('title'),
            description = kwargs.get('description'),
            color = 0xddbef8
        )


class TicketEmbed(BaseEmbed):
    def __init__(
        self, **kwargs
    ) -> None:
        super().__init__(
            title = kwargs.get('title'),
            description = kwargs.get('description'),
            color=0xe91e63
        )


class ExceptionEmbed(disnake.Embed):
    def __init__(
        self, message: str
    ) -> None:
        super().__init__(
            title=_("exception_title"),
            description=message,
            color=0xe74c3c
        )
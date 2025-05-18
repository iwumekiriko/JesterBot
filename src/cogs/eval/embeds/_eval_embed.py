from src.utils.ui import BaseEmbed


class EvalEmbed(BaseEmbed):
    def __init__(
        self, message: str
    ) -> None:
        super().__init__(
            title = "Evaled!",
            description = message,
            color=0x38e5ce
        )
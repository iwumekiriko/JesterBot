import disnake
import uuid
from typing import List, Optional, Any, Union

from src.utils._exceptions import ModalTimeoutException


class ModalTextInput(disnake.ui.TextInput):
    def __init__(
        self,
        label: str,
        style: disnake.TextInputStyle
                = disnake.TextInputStyle.short,
        placeholder: Optional[str] = None,
        value: Optional[str] = None,
        required: bool = True,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None
    ) -> None:
        super().__init__(
            label=label,
            custom_id=str(uuid.uuid4()),
            style=style,
            placeholder=placeholder,
            value=value,
            required=required,
            min_length=min_length,
            max_length=max_length
        )


class BaseModal(disnake.ui.Modal):
    def __init__(
        self,
        title: str,
        components: List[ModalTextInput],
        interaction: Union[
                disnake.MessageCommandInteraction,
                disnake.ApplicationCommandInteraction],
        timeout: int = 600
    ) -> None:
        super().__init__(
            title=title,
            components=components,
            custom_id=f"custom_modal-{interaction.id}",
            timeout=timeout
        )
        self.interaction = interaction

    async def receive_data(self) -> List[Any]:
        inter = self.interaction
        await inter.response.send_modal(self)
        try:
            modal_inter: disnake.ModalInteraction = await inter.bot.wait_for(
                "modal_submit",
                check=lambda m: m.custom_id == self.custom_id,
                timeout=self.timeout
            )
        except:
            await self._timeout_handler()

        inter.response = modal_inter.response # type: ignore
        text_values = modal_inter.text_values
        data: List[Any] = [
            text_values[child.custom_id] for component
             in self.components for child in component]
        data.insert(0, modal_inter)
        return data
    
    async def on_error(
        self,
        error: Exception,
        interaction: disnake.ModalInteraction
    ) -> None:
        return await super().on_error(error, interaction)
    
    async def _timeout_handler(self) -> None:
        raise ModalTimeoutException()



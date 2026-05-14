import disnake
import uuid
from typing import List, Optional, Any, Sequence, Union

from src.utils._exceptions import ModalTimeoutException


class ModalTextDisplay(disnake.ui.TextDisplay):
    def __init__(
        self,
        content: str
    ) -> None:
        super().__init__(
            content = content
        )


class ModalTextInput(disnake.ui.TextInput):
    def __init__(
        self,
        style: disnake.TextInputStyle
                = disnake.TextInputStyle.short,
        placeholder: Optional[str] = None,
        value: Optional[str] = None,
        required: bool = True,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None
    ) -> None:
        super().__init__(
            custom_id=str(uuid.uuid4()),
            style=style,
            placeholder=placeholder,
            value=value,
            required=required,
            min_length=min_length,
            max_length=max_length
        )


class ModalSelectMenu(disnake.ui.Select):
    def __init__(
        self,
        options: list[disnake.SelectOption],
        placeholder: Optional[str] = None,
        min_values: int = 1,
        max_values: int = 1,
        disabled: bool = False,
        required: bool = True
    ) -> None:
        super().__init__(
            custom_id=str(uuid.uuid4()),
            options=options,
            placeholder=placeholder,
            disabled=disabled,
            required=required,
            min_values=min_values,
            max_values=max_values
        )


class ModalLabel(disnake.ui.Label):
    def __init__(
        self,
        text: str,
        component: Union[ModalTextInput, ModalSelectMenu],
        description: Optional[str] = None
    ) -> None:
        super().__init__(
            text=text,
            component=component,
            description=description
        )


class BaseModal(disnake.ui.Modal):
    def __init__(
        self,
        title: str,
        components: Sequence[Union[ModalTextDisplay, ModalLabel]],
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
        self._components = components

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
        components_data = {}
        for label in modal_inter.data["components"]:
            component = label["component"]
            components_data[component["custom_id"]] = component

        values = []

        for item in self._components:
            if isinstance(item, ModalLabel):
                component = item.component

            else:
                component = item 

            if isinstance(component, ModalTextDisplay):
                continue

            raw = components_data.get(component.custom_id)

            if raw is None:
                values.append(None)
                continue

            if isinstance(component, ModalTextInput):
                values.append(raw.get("value"))

            elif isinstance(component, ModalSelectMenu):
                values.append(raw.get("values", []))

        values.insert(0, modal_inter)
        return values

    async def on_error(
        self,
        error: Exception,
        interaction: disnake.ModalInteraction
    ) -> None:
        return await super().on_error(error, interaction)

    async def _timeout_handler(self) -> None:
        raise ModalTimeoutException()
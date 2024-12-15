from disnake import MessageCommandInteraction, TextInputStyle
from typing import Callable, Optional
import disnake

# from .._role_purchase import (
#     shop_select
# )

from src.localization import get_localizator


_ = get_localizator("shop")


class CoolView(disnake.ui.View):
    def __init__(
        self
    ) -> None:
        super().__init__(timeout=None)
        self.shop_options: dict[
            tuple[str, Optional[str]],
            Callable
        ] = {
            ("1", "1309328136302886992"): get_role,
            ("2", "1309329395336351767"): get_role,
            ("3", "1309329505059340398"): get_role
        }
        
        self.add_item(CoolSelect(self.shop_options))


class CoolSelect(disnake.ui.Select):
    view: CoolView

    def __init__(self, shop_options: dict) -> None:
        super().__init__(
            custom_id="open-shop-menu",
            options=[disnake.SelectOption(
                label=name, value=i)
                for name, i in shop_options])
        
    async def callback(
        self,
        interaction: disnake.MessageCommandInteraction
    ) -> None:
        id = self.values[0]
        await next((value for key, value in self.view.shop_options.items()
              if key[0] == id), get_role)(interaction, interaction.user, int(id))
        await interaction.response.send_message("Вы успешно преобрели роль <@&"+id+">", ephemeral = True)


async def get_role(interaction: MessageCommandInteraction, member:disnake.Member, id:int):
    role = disnake.utils.get(member.guild.roles, id = id)  
    await member.add_roles(role) 
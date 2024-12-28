import disnake

# from .._role_purchase import (
#     shop_select
# )

from .._api_interaction import zabral_dengi
from src.localization import get_localizator


_ = get_localizator("shop")


class ShopRolesView(disnake.ui.View):
    def __init__(
        self,
        guild_id: int,
        roles: dict
    ) -> None:
        super().__init__(timeout=None)

        self.guild_id = guild_id
        self.shop_roles = roles
        roles_ids = list(self.shop_roles.keys())

        self.add_item(RolesSelect(roles_ids))


class RolesSelect(disnake.ui.Select):
    view: ShopRolesView

    def __init__(self, roles_ids: list[int]) -> None:
        super().__init__( 
            custom_id="open-shop-menu",
            options=[disnake.SelectOption(
                label = str(i), value = str(z))
                for i, z in enumerate(roles_ids, start = 1)
            ])
        
    async def callback(
        self,
        interaction: disnake.MessageCommandInteraction
    ) -> None:
        role_id = int(self.values[0])
        error = await zabral_dengi(interaction.guild_id, interaction.user.id, self.view.shop_roles[role_id]) # type: ignore
        if error:
            await interaction.response.send_message(error, ephemeral = True)
            return
        await set_role(interaction.user, role_id) # type: ignore
        await interaction.response.send_message(f"Вы успешно преобрели роль <@&{role_id}>", ephemeral = True)


async def set_role(member:disnake.Member, role_id:int):
    role = member.guild.get_role(role_id) 
    await member.add_roles(role) # type: ignore
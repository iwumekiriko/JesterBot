from disnake import MessageCommandInteraction, TextInputStyle
from .views._shop_roles_view import ShopRolesView
from ._api_interaction import get_roles

import disnake

from src.localization import get_localizator
from .embeds import ShopEmbed


_ = get_localizator("shop")

async def shop_select(interaction: MessageCommandInteraction):
        await interaction.response.send_message(
            ephemeral=True,
            embed = ShopEmbed(
                title = _("shop_embed_title"),
                description = _("shop_embed_description")
            ),
            view = ShopRolesView(
                guild_id=interaction.guild_id, # type: ignore
                roles = await get_roles(interaction.guild_id) # type: ignore
            ))
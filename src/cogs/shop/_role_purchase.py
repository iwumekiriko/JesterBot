from disnake import MessageCommandInteraction, TextInputStyle
from .views._123_cool_view import CoolView

import disnake

from src.localization import get_localizator
from src.utils._embeds import ShopEmbed


_ = get_localizator("shop")

async def shop_select(interaction: MessageCommandInteraction):
        await interaction.response.send_message(
            ephemeral=True,
            embed = ShopEmbed(
                title = _("shop_embed_title"),
                description = _("shop_embed_description")
            ),
            view = CoolView(
                    
            ))
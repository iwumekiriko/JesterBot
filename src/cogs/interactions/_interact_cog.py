import disnake
from disnake.ext import commands

from src.bot import JesterBot
from src.utils._converters import inter_member
from ._interactions_choice import InteractionActions, InteractionTypes
from src.localization import get_localizator
from src.utils.ui import BaseEmbed
from ._api_interaction import get_gif


_ = get_localizator("interactions.common")


limits = {
    "kiss": 30,
    "hug": 30,
    "pat": 30,
    "hit": 15
}


class UserInteractionsCog(commands.Cog):
    def __init__(self, bot: JesterBot):
        self.bot = bot

    @commands.slash_command(description=_("user_interaction_desc"))
    async def interact(
        self,
        interaction: disnake.GuildCommandInteraction,
        member: disnake.Member = commands.Param(
            converter=inter_member, description=_("user_interaction_member_param")),
        action = commands.Param(
            choices={choice.translated_name: choice.name.lower() for choice in InteractionActions},
            description=_("user_interaction_action_param")),
        type = commands.Param(
            choices={type.translated_name: type.name.lower() for type in InteractionTypes},
            description=_("user_interaction_type_param"))
    ) -> None:
        await interaction.response.send_message(
            content=member.mention,
            embed=BaseEmbed(
                description=_(action,
                            command_user=interaction.user.id,
                            command_target=member.id)
            ).set_image(await get_gif(action, type, limit=limits[action])))



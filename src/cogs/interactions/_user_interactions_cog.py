import disnake
from disnake.ext import commands

from src.bot import JesterBot
from src.utils._convertes import inter_member
from ._interactions_choice import InteractionChoices, InteractionType
from src.localization import get_localizator
from src.utils._embeds import BaseEmbed
from ._api_interaction import get_gif


_ = get_localizator("interactions")


limits = {
    "kiss": 30,
    "hug": 30,
    "pat": 30,
    "hit": 15
}


class UserInteractionsCog(commands.Cog):
    def __init__(self, bot: JesterBot):
        self.bot = bot

    @commands.slash_command()
    async def user_interaction(
        self,
        interaction: disnake.GuildCommandInteraction,
        member: disnake.Member=commands.Param(converter=inter_member),
        choice=commands.Param(
            choices={choice.translated_name: choice for choice in InteractionChoices}),
        type=commands.Param(
            choices={type.translated_name: type for type in InteractionType})
    ) -> None:
        """
        Взаимодействуйте с пользователем

        Parameters
        ----------
        member: Участник, с которым вы хотите взаимодействовать
        choice: Действие, которое вы хотите сделать
        type: Стилизация гиф картинки
        """
        await interaction.response.send_message(
            content=member.mention,
            embed=BaseEmbed(
                description=_(choice,
                            command_user=interaction.user.id,
                            command_target=member.id)
            ).set_image(await get_gif(choice, type, limit=limits[choice])))



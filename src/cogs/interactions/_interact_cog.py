from typing import List
import pandas as pd
from io import BytesIO

import disnake
from disnake.ext import commands

from src.bot import JesterBot
from src.localization import get_localizator
from src.logger import get_logger

from src.utils._converters import inter_member
from ._interactions_choice import InteractionActions, InteractionTypes
from src.models.interactions import InteractionsAsset
from src.utils.ui import BaseEmbed
from ._api_interaction import get_gif, upload_gifs
from src.utils._permissions import for_admins
from src.utils.ui import SuccessEmbed, ExceptionEmbed


logger = get_logger()
_ = get_localizator("interactions.common")


ACCEPTABLE_DF_COLUMNS = ['Url', 'Action', 'Type']
ACCEPTABLE_ACTIONS = [action.name.lower() for action in InteractionActions]
ACCEPTABLE_TYPES = [type.name.lower() for type in InteractionTypes]


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
            choices={choice.translated_name: str(choice.value) for choice in InteractionActions},
            description=_("user_interaction_action_param")),
        type = commands.Param(
            choices={type.translated_name: str(type.value) for type in InteractionTypes},
            description=_("user_interaction_type_param"))
    ) -> None:
        action = InteractionActions(int(action))
        type = InteractionTypes(int(type))

        await interaction.response.send_message(
            content=member.mention,
            embed=BaseEmbed(    
                description=_(action.name.lower(),
                            command_user=interaction.user.id,
                            command_target=member.id)
            ).set_image(await get_gif(
                interaction.guild.id,
                action.value,
                type.value
            )))

    @commands.slash_command(**for_admins, description=_("interactions-gifs-upload_desc"))
    async def _ug(
        self,
        interaction: disnake.GuildCommandInteraction,
        attachment: disnake.Attachment = commands.Param(
            description=_("interactions-gifs-upload_attachment_param"))
    ) -> None:
        if (attachment.filename and not 
            ("csv" in attachment.filename or "xlsx" in attachment.filename)
        ):
            await interaction.response.send_message(
                embed=ExceptionEmbed(error_msg=_("wrong_file_type_error")),
                ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)
        extension = attachment.filename.split('.')[-1]

        match (extension):
            case "csv":
                df = pd.read_csv(BytesIO(await attachment.read()))
            case "xlsx":
                df = pd.read_excel(BytesIO(await attachment.read()))

        if not self.is_dataframe_correct(df):
            await interaction.followup.send(
                embed=ExceptionEmbed(error_msg=_("wrong_dataframe_structure_error")),
                ephemeral=True)

        gifs = await self.handle_dataframe(df)
        await upload_gifs(interaction.guild.id, gifs)
        await interaction.followup.send(
            embed=SuccessEmbed(success_msg=_("success_upload_response")),
            ephemeral=True)

    async def handle_dataframe(self, df: pd.DataFrame) -> List[InteractionsAsset]:
        if not (df.columns.to_list() == ['Url', 'Action', 'Type']):
            return []

        cleaned_df = df.dropna()
        interactions_assets: List[InteractionsAsset] = []
        for _, row in cleaned_df.iterrows():
            if not (i_action := str(row['Action']).lower()) in ACCEPTABLE_ACTIONS:
                continue

            if not (i_type := str(row['Type']).lower()) in ACCEPTABLE_TYPES:
                continue

            url = row['Url']
            action = InteractionActions[i_action.upper()] 
            type = InteractionTypes[i_type.upper()]
            interactions_assets.append(InteractionsAsset(url, action, type))

        return interactions_assets

    def is_dataframe_correct(self, df: pd.DataFrame) -> bool:
        if not (df.columns.to_list() == ACCEPTABLE_DF_COLUMNS):
            return False
        
        return True

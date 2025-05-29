import io
import disnake
from disnake.ext import commands

from src.bot import JesterBot
from src.utils._permissions import for_moders
from src.utils._converters import is_member, user_avatar
from src.localization import get_localizator
from ._time_choices import TimeChoices
from src.logger import get_logger
from src.utils._time import current_time


_ = get_localizator("clean.common")
logger = get_logger()


class CleanCog(commands.Cog):
    def __init__(self, bot: JesterBot) -> None:
        self.bot = bot

    @commands.slash_command(**for_moders, description=_("clean_desc"))
    async def clean(
        self,
        interaction: disnake.GuildCommandInteraction,
        amount: int = commands.Param(default=20, description=_("clean_amount_param")),
        member: disnake.Member = commands.Param(converter=is_member, default=None, description=_("clean_member_param")),
        time = commands.Param(
            choices={choice.translated_name: choice for choice in TimeChoices}, default=None, description=_("clean_time_param")),
    ) -> None:
        channel = interaction.channel
        if not isinstance(channel, (disnake.abc.GuildChannel, disnake.Thread)):
            raise commands.BadArgument(_("clean_wrong_channel_type_error"))

        try:
            await interaction.response.defer(ephemeral=True)

            check = lambda m: m.author == member if member else True
            after = TimeChoices(time).get_time() if time else None
            deleted = await channel.purge(limit=amount, check=check, after=after)
            d_count = len(deleted)

            await interaction.followup.send(
                    content=_("cleaned", count=d_count), ephemeral=True)


            d_file = _make_file(channel, deleted) if len(deleted) > 0 else None

            logger.warning("Сообщения были удалены из канала: <#%d>\n\n-# Количество: %d\n-# Модератор: <@%d>",
                            interaction.channel.id, d_count, interaction.author.id,
                            extra={"user_avatar": user_avatar(jester=True), "type": "message",
                                    "files": [d_file], "guild_id": interaction.guild.id})

        except Exception as e:
            raise commands.BadArgument(str(e))


def _make_file(channel, deleted: list[disnake.Message]) -> disnake.File:
    m_data = f"Канал: {channel.name} | {channel.id}\n"
    m_data += f"Время: {current_time().strftime('%d-%B-%Y — %H:%M:%S')}\n\n"
    m_data += "---------------------------\n\n"
    for message in deleted:
        m_data += f"Автор: {message.author}\n"
        m_data += f"Контент: {message.content}\n"
        m_data += ("Вложения:" + ''.join([('\n     ' + f'{i}. {attachment.url}') 
                    for i, attachment in enumerate(message.attachments, 1)]) + "\n")
        m_data += f"Дата отправки: {message.created_at.strftime('%d-%B-%Y — %H:%M:%S')}\n\n"

    m_file = io.BytesIO(m_data.encode('utf-8', errors='ignore'))
    m_file.seek(0)

    d_file = disnake.File(m_file, "deleted_messages.txt")

    return d_file
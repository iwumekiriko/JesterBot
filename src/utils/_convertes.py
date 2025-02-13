import disnake
from disnake.ext import commands

from src.localization import get_localizator


_ = get_localizator()


def is_member(
    inter: disnake.ApplicationCommandInteraction,
    arg: disnake.User | disnake.Member
) -> disnake.Member:
    """Chosen user must be a member."""
    if not isinstance(arg, disnake.Member):
        raise commands.BadArgument(_("not_found_member_error"))
    return arg


def bot_excluding(
    inter: disnake.ApplicationCommandInteraction,
    arg: disnake.Member | disnake.User
) -> disnake.Member:
    """Chosen user can't be a bot."""
    member = is_member(inter, arg)
    if member.bot:
        raise commands.BadArgument(_("not_for_bot_error"))
    return member


def self_excluding(
    inter: disnake.ApplicationCommandInteraction,
    arg: disnake.Member | disnake.User
) -> disnake.Member:
    """Chosen user can't be self."""
    member = is_member(inter, arg)
    if member == inter.user:
        raise commands.BadArgument(_("not_for_self_error"))
    return member


def inter_member(
    inter: disnake.ApplicationCommandInteraction,
    arg: disnake.Member | disnake.User
) -> disnake.Member:
    """Chosen user must be: a member + not a bot + not self"""
    _not_bot = bot_excluding(inter, arg)
    _not_self_nor_bot = self_excluding(inter, _not_bot)
    return _not_self_nor_bot


def user_avatar(user_id: int = 0, jester: bool = False) -> str | None:
    """
    Returns avatar url from user id.

    Args:
        user_id (int): user whose avatar needs to be returned
        jester (bool): if avatar should be from bot

    Returns:
        str | None: avatar.url
    """
    from src.bot import bot
    if user_id == 0 and not jester: return None 

    return (bot.get_user(user_id).display_avatar.url # type: ignore
            or bot.get_user(user_id).default_avatar.url # type: ignore
            if not jester else bot.user.avatar.url) # type: ignore

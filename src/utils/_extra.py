from typing import Optional

from disnake import Guild, Member, Role
from disnake.utils import get

from src.settings import BASE_GUILD_ID


def get_discord_role_by_id(
    guild_id: int,
    role_id: int
) -> Optional[Role]:
    from src.bot import bot

    guild = bot.get_guild(guild_id) or bot.get_guild(BASE_GUILD_ID)
    return get(guild.roles, id=role_id) # type: ignore


async def add_role_with_id(
    guild: Guild,
    member: Member,
    role_id: int
) -> bool:
    """
    Adds a role to the member by id.

    Args:
        guild (disnake.Guild): role's guild
        member (disnake.Member): member to add role
        role_id (int): role's id in guild

    Returns:
        bool: has role been added?
    """
    from src.cogs.inventory._api_interaction import get_member_roles

    role = get(guild.roles, id = role_id)

    if not role:
        return False

    if role in member.roles:
        return False

    inventory_roles = await get_member_roles(guild.id, member.id)
    roles_to_remove_ids = [r.guild_role_id for r in inventory_roles 
                          if r.guild_role_id != role_id]
    roles_to_remove = [r for r in guild.roles if r.id in roles_to_remove_ids]

    await member.add_roles(role)
    await member.remove_roles(*roles_to_remove)
    return True


async def remove_role_with_id(
    guild: Guild,
    member: Member,
    role_id: int
) -> bool:
    """
    Removes a role from the member by id.

    Args:
        guild (disnake.Guild): Role's guild.
        member (disnake.Member): Member to remove role.
        role_id (int): Role's id in guild.

    Returns:
        bool: Has role been removed?
    """
    role = get(guild.roles, id = role_id)
    if not role:
        return False

    if role not in member.roles:
        return False

    await member.remove_roles(role)
    return True


def make_formatted_slash_command(
    command_name: str
) -> Optional[str]:
    """
    Args:
        command_name (str): Slash command's name.
    
    Returns:
        str: Formatted slash command.

    Examples:
        >>> make_formatted_slash_command("lootboxes")
        </lootboxes:1234567890>
    """
    from src.bot import bot
    command = next(command for command in bot.global_slash_commands
                    if command.name == command_name)
    if not command:
        return None

    return f"</{command.name}:{command.id}>"

from disnake import Permissions


for_admins = {
    'dm_permission': False,
    'default_member_permissions': Permissions(administrator=True)
}

for_moders = {
    'dm_permission': False,
    'default_member_permissions': Permissions(manage_channels=True)
}
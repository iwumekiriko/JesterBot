# -------------------

# Experience parameters

# Amount of experience a member gets after sending a message. [default: 3]
EXP_FOR_MESSAGE = 3
# Amount of experience a member gets after spendning a minute in a voice channel. [default: 1]
EXP_FOR_VOICE_MINUTE = 1

# -------------------

# Roles for tickets mentions

# Support guild role 
SUPPORT_ROLE_ID = 0
# Moderator guild role
MODERATOR_ROLE_ID = 0
# Developer guild role
DEVELOPER_ROLE_ID = 0

# -------------------

# Auxiliary parameters needed for activity cog

GENERAL_CHANNEL_ID = 0
OFFTOP_CHANNEL_ID = 0

# -------------------

# Shop parameters

# Channel containing persistent shop view
SHOP_CHANNEL_ID = 0
# Message with persistent shop view
# Wrong id or None leads to new message creation in the channel
SHOP_MESSAGE_ID = 0

# -------------------

# Tickets parameters

# Channel containing persistent tickets view
TICKET_CHANNEL_ID = 0
# Message with persistent ticket view
# Wrong id or None leads to new message creation in the channel
TICKET_MESSAGE_ID = 0
# Channel containing after closing info about tickets
TICKET_REPORT_CHANNEL_ID = 0

# -------------------

# Custom voice channels parameters

# Voice Channel serving as a transition to a custom channel
CUSTOM_VOICE_CREATION_CHANNEL_ID = 0
# Category which contains transition channel 
CUSTOM_VOICE_CATEGORY_ID = 0
# Amount of seconds after which the custom channel will be deleted [default: 30]
CUSTOM_VOICE_DELETION_TIME = 30

# -------------------

# Logs parameters

# Webhook with info about members using slash commands 
COMMAND_INTERACTIONS_WEBHOOK_URL = ""
# Webhook with info about editing and deleting messages
MESSAGES_WEBHOOK_URL = ""
# Webhook with info about creating, acception and closing tickets
TICKETS_WEBHOOK_URL = ""
# Webhook with info about members joins and leaves
GUILD_WEBHOOK_URL = ""
# Webhook with info about members changing avatars and nicknames
MEMBERS_WEBHOOK_URL = ""
# Webhook with else info
ELSE_WEBHOOK_URL = ""

# -------------------

# Lootboxes parameters

# Amount of coins to buy Roles Lootbox Key [default: 3000]
ROLES_LOOTBOX_KEYS_PRICE = 3000
# Amount of coins to buy Roles Lootbox Key [default: 3000]
BACKGROUNDS_LOOTBOX_KEYS_PRICE = 3000

# -------------------

# Economy parameters

# Emoji to represent default currency [🪙]
DEFAULT_CURRENCY_ICON = "🪙"
# Emoji to represent donate currency [🥐]
DONATE_CURRENCY_ICON = "🥐"
# Amount of coins to get from /daily
DAILY_BONUS = 300
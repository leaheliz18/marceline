import os
from dotenv import load_dotenv
import discord

# load environment variables from .env
load_dotenv()

# token: your discord bot token
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# colour: embed theme colour
THEME_COLOUR = discord.Color.from_str("#acc8dd")
ID_ROLE_ADMIN = 1367261098352447518
ID_CHANNEL_ANNOUNCEMENT = 1368348461459705856
ID_CHANNEL_ROLES = 1

# intents: discord gateway access configuration
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.reactions = True
intents.message_content = True
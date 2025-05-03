# main.py
import discord
from discord.ext import commands
from config import DISCORD_TOKEN, THEME_COLOUR, ID_ROLE_ADMIN, ID_CHANNEL_ANNOUNCEMENT, intents
from data.roles import reaction_roles_colours_pastel, reaction_roles_games, role_map_emoji, role_map_game
from utils.storage import load_reaction_ids, save_reaction_ids

import json

REACTION_IDS = load_reaction_ids()

bot = commands.Bot(command_prefix="!", intents=intents)

# !info : returns a help menu
@bot.command(name="info")
async def bot_help(ctx):
    embed = discord.Embed(
        title="˗ˏ˗ ×ㅤㅤhelp menuㅤㅤ× ˗ˎ˗",
        description="Here are the available commands:",
        color=THEME_COLOUR
    )
    embed.add_field(name="!setup_reaction_roles", value="Set up the reaction roles message.", inline=False)
    embed.add_field(name="!help", value="Display this help menu.", inline=False)
    embed.set_footer(text="jerry sucks")
    await ctx.send(embed=embed)

# !reaction-role-embed
@bot.command(name="setup_reaction_roles")
@commands.has_role(ID_ROLE_ADMIN)
async def reaction_role_embed(ctx): 
    from utils.helpers import make_description

    lines_colour_pastel = [make_description(ctx, name, id_emoji, id_role) for name, (id_emoji, id_role) in reaction_roles_colours_pastel.items()]
    lines_games = [make_description(ctx, name, id_emoji, id_role) for name, (id_emoji, id_role) in reaction_roles_games.items()]

    embed_channel = discord.Embed(title="", description="", color=THEME_COLOUR)
    embed_colour_pastel = discord.Embed(
      title="˗ˏ˗ ×ㅤㅤpastel coloursㅤㅤ× ˗ˎ˗",
      description=("\n".join(lines_colour_pastel)+ "\n\n<:paw:1368344059055312906><:starline:1368343900854554644><:paw:1368344059055312906><:starline:1368343900854554644><:paw:1368344059055312906><:starline:1368343900854554644><:paw:1368344059055312906><:starline:1368343900854554644><:paw:1368344059055312906><:starline:1368343900854554644><:paw:1368344059055312906>"),
      color=THEME_COLOUR
    )
    embed_games = discord.Embed(
      title="˗ˏ˗ ×ㅤㅤgame pingsㅤㅤ× ˗ˎ˗",
      description=("\n".join(lines_games)+ "\n\n<:paw:1368344059055312906><:starline:1368343900854554644><:paw:1368344059055312906><:starline:1368343900854554644><:paw:1368344059055312906><:starline:1368343900854554644><:paw:1368344059055312906><:starline:1368343900854554644><:paw:1368344059055312906><:starline:1368343900854554644><:paw:1368344059055312906><:starline:1368343900854554644><:paw:1368344059055312906><:starline:1368343900854554644><:paw:1368344059055312906><:starline:1368343900854554644><:paw:1368344059055312906>"),
      color=THEME_COLOUR
    )

    embed_channel.set_image(url="https://media.discordapp.net/attachments/1100555348466741279/1368050518483800116/roles.png?ex=6816cfd4&is=68157e54&hm=ed49a11bd01e00e9767a858976d35a3d22c5910c2f9e8551549b551b5c040273&=&format=webp&quality=lossless&width=1522&height=856")
    await ctx.send(embed=embed_channel)

    msg_colour_pastel = await ctx.send(embed=embed_colour_pastel)
    msg_games = await ctx.send(embed=embed_games)

    from utils.helpers import add_reactions
    await add_reactions(bot, msg_colour_pastel, reaction_roles_colours_pastel)
    await add_reactions(bot, msg_games, reaction_roles_games)

    global REACTION_IDS
    REACTION_IDS = [msg_colour_pastel.id, msg_games.id]
    save_reaction_ids(REACTION_IDS)

# !announcements
@bot.command(name="announcement")
@commands.has_role(ID_ROLE_ADMIN)
async def announcement(ctx, *, args):
    inputs = [input.strip() for input in args.split('|')]
    if len(inputs) < 2:
        await ctx.send("correct usage: `!announcement <title> | <description> | <optional image> | <optional footer>`")
        return
    title = f"˗ˏ˗ ×ㅤㅤ{inputs[0]}ㅤㅤ× ˗ˎ˗"
    desc = inputs[1]
    img_url = inputs[2] if len(inputs) > 2 and inputs[2].startswith("http") else None
    footer = inputs[3] if len(inputs) > 3 else None

    embed_announcement = discord.Embed(
        title=title,
        description=desc,
        color=THEME_COLOUR
    )

    if img_url:
        embed_announcement.set_image(url=img_url)
    if footer:
        embed_announcement.set_footer(text=footer)

    channel_announcement = bot.get_channel(ID_CHANNEL_ANNOUNCEMENT)
    if channel_announcement:
        await channel_announcement.send(embed=embed_announcement)

# add roles on reaction
@bot.event
async def on_raw_reaction_add(payload):
    if not REACTION_IDS or payload.message_id not in REACTION_IDS:
        return
    role_id = role_map_emoji.get(payload.emoji.id) or role_map_game.get(payload.emoji.id)
    if role_id:
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        role = guild.get_role(role_id)
        print(f"Trying to add role: {role.name} ({role.id}) to {member.display_name} ({member.id})")
        await member.add_roles(role)
        print("Role successfully added (or no error)")

# remove roles on reaction
@bot.event
async def on_raw_reaction_remove(payload):
    if not REACTION_IDS or payload.message_id not in REACTION_IDS:
        return
    role_id = role_map_emoji.get(payload.emoji.id) or role_map_game.get(payload.emoji.id)
    if role_id:
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        role = guild.get_role(role_id)
        await member.remove_roles(role)

# welcome message on member join
@bot.event
async def on_member_join(member):
    channel = member.guild.get_channel(1361812883771490485)
    if channel:
        embed_welcome = discord.Embed(
            title="<:pbheart:1368249862566707230>ㅤwelcome to casual arsonistsㅤ<:pbheart:1368249862566707230>",
            description= (
                "・・・・・・・・・・・・・・・・・・・\n"
                f"nice to meet you {member.mention}!\n"
                "have a good time and don't forget to claim your roles at <#1368345992927379507>!\n"
                "・・・・・・・・・・・・・・・・・・・\n"
            ),
            color=THEME_COLOUR
        )
        await channel.send(embed=embed_welcome)

# no perms to use command
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("you don’t have permission to use that command !")


bot.run(DISCORD_TOKEN)

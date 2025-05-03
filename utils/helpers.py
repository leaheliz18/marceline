# helpers.py
def make_description(ctx, name, emoji_id, role_id):
    """format one line of role description using the custom emoji and @role mention"""
    role = ctx.guild.get_role(role_id)
    return f"ㅤㅤ« <:pbheart:1368249862566707230> »ㅤ◌ㅤ<:{name}:{emoji_id}> {role.mention if role else '`missing role`'}"

async def add_reactions(bot, msg, emoji_map):
    """add all emoji reactions from emoji_map to the given message"""
    for name, (emoji_id, _) in emoji_map.items():
        emoji = bot.get_emoji(emoji_id)
        if emoji:
            await msg.add_reaction(emoji)
        else:
            await msg.add_reaction(f"<:{name}:{emoji_id}>")

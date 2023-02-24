# -*- coding: utf-8 -*-

import discord, os, json, subprocess
from discord.ext import commands
from random import randrange
from pathlib import Path

intents = discord.Intents.default()
intents.dm_messages = True
intents.message_content = True
intents.members = True
intents.guild_messages = True
intents.guild_reactions = True

bot = commands.Bot(command_prefix='!', intents=intents)



@bot.event
async def on_message(m):
    print(m)
    if m.author.bot:
        print('bot')
        print(m.content)
        try:
            print(m.embeds)
            for embed in m.embeds:
                print(embed.to_dict(), '\n\n\n\n\n')
                if 'Cx7#9314' in list(embed.to_dict().values()):
                    await m.delete()
        except Exception as e:
            print(f"An error occurred: {e}")



token = os.environ.get('DISCORD_BOT_TOKEN')

if token is None:
    print(token)
else:
    bot.run(token)



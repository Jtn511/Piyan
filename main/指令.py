# -*- coding: utf-8 -*-

import discord, os, json, subprocess
from discord.ext import commands
from random import randrange
from pathlib import Path

intents = discord.Intents.default()
intents.dm_messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

def load(path):
    if not path.exists():
        path.touch()
    with open(path, 'r', encoding = 'utf8') as f:
        return json.load(f)


@bot.event
async def on_message(m):
    if m.author.bot:
        return
    
    if '<@1043082295764078652>' in m.content: # 被標記
        call = m.content.split('1043082295764078652>')[1].strip().split(' ')[0]
        
        if call  == "公告": # piyanCall 不在這
            message = ""
            for i in range(len(replyDict[call])):
                message += replyDict[call][i] + "\n"
            await m.reply(message)
            return
    
token = os.environ.get('DISCORD_BOT_TOKEN')

if token is None:
    print(token)
else:
    bot.run(token)

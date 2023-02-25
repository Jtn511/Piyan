# -*- coding: utf-8 -*-

import discord, os, json, subprocess
from discord.ext import commands
from random import randrange
from pathlib import Path

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

def load(path):
    if not path.exists():
        path.touch()
    with open(path, 'r', encoding = 'utf8') as f:
        return json.load(f)

async def announcement(string):
    channel = bot.get_channel(1016736583157821453)  # 這裡替換成你的頻道 ID
    #channel = bot.get_channel(1078382554400432242)  # 屁眼
    with open('announcement.png', 'rb') as f:
        await channel.send(string, file=discord.File(f))
    return

@bot.event
async def on_message(call):
    admin = load(Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/VIP/admin.json'))
    if call.guild:  # DM才繼續
        return
    if call.author.id in admin: # 權限檢查
        if '<@1043082295764078652>' in call.content:    # 標記Bot
            if call.content.split('>')[1].strip() == '公告': # 公告指令
                r = call.reference.resolved 
                if r:   # 回覆目標存在
                    await announcement(r.content)
                    
                    

token = os.environ.get('DISCORD_BOT_TOKEN')

if token is None:
    print(token)
else:
    bot.run(token)

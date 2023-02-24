import discord, os, json
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
        replyDict = load(Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/command_list/reply_text.json'))
        call = m.content.split('1043082295764078652>')[1].strip().split(' ')[0]
        
        if call in replyDict: # piyanCall 不在這
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

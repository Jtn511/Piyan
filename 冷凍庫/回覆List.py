import discord, os, json, re
from discord.ext import commands
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

def dump(data, path):
    with open(path, 'w', encoding = 'utf8') as f:
        json.dump(data, f, ensure_ascii=False)

async def piyanList(m):

    dictPath = Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/reply_dictionary', f'{m.guild.id}/dictionary.json')
    dictPath.parent.mkdir(parents=True, exist_ok=True)

    try:
        dictionary = load(dictPath)
    except:
        dictionary = {}

    replylist = []

    replyKey = ""
    replyValue = ""
    for i in dictionary:
        replyKey += f"{i}\n"
        replyValue += f"{dictionary[i][0][:15]}\n"


    embedVar = discord.Embed(title="Piyan List", color=0x4c9ce0)
    embedVar.add_field(name="關鍵字", value=replyKey, inline=True)
    embedVar.add_field(name="回傳值", value=replyValue, inline=True)
    await m.channel.send(embed=embedVar)

    return

@bot.event
async def on_message(m):
    if m.author.bot:
        return
    
    if '<@1043082295764078652>' in m.content:
        if m.content.split('>')[1].strip().split(' ')[0] in ["清單", "list", "List", "LIST"]:
            await piyanList(m)

token = os.environ.get('DISCORD_BOT_TOKEN')

if token is None:
    print(token)
else:
    bot.run(token)

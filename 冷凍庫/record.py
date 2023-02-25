import discord, requests, os
from discord.ext import commands
from pathlib import Path
from datetime import datetime

intents = discord.Intents.default()
intents.dm_messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def record_dm(message):
    if isinstance(message.channel, discord.DMChannel) and message.author != bot.user:
        t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{t} | {message.author}: {message.content}")
        DM_path = Path('C:\\Users\\jtn91\\OneDrive\\桌面\\Piyan\\Chat\\DM', f'{message.author.id}.txt')
        DM_path.parent.mkdir(parents=True, exist_ok=True)
        with DM_path.open('a', encoding='utf-8') as f:
            f.write(f"{t} | {message.author}: {message.content}\n")

    for attachment in message.attachments:
        if attachment.content_type.startswith('image/'):
            response = requests.get(attachment.url)
            with open(attachment.filename, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {attachment.filename}")
    return

async def record_guild(message):
    guild_path = Path('C:\\Users\\jtn91\\OneDrive\\桌面\\Piyan\\Chat\\Guild', f'{message.guild.name}', f'{message.channel.name}.txt')
    guild_path.parent.mkdir(parents=True, exist_ok=True)
    
    t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with guild_path.open('a', encoding='utf-8') as f:
        f.write(f"{t} | {message.author}: {message.content}\n")
    return

@bot.event
async def on_ready():
    print('Recording...')

@bot.event
async def on_message(message):
    if message.guild:
        await record_guild(message)
    else:
        await record_dm(message)

token = os.environ.get('DISCORD_BOT_TOKEN')

if token is None:
    print(token)
else:
    bot.run(token)

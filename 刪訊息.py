import discord, os
from discord.ext import commands
from pathlib import Path
import json

intents = discord.Intents.default()
intents.dm_messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

VIP = [634414049815166997] #868565069460545536]

def load(path):
    if not path.exists():
        path.touch()
    with open(path, 'r', encoding = 'utf8') as f:
        return json.load(f)

@bot.event
async def on_message(call):
    admin = load(Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/VIP/admin.json'))
    if call.author.id in admin:
        if call.content.startswith('ㄇ'):
        # 取得指定頻道的訊息
            if call.reference:
                await call.delete()
                await call.reference.resolved.delete()
            else:
                try:
                    Guild, Channel, Message = map(int, call.content.split('channels/')[1].split('/'))

                    channel = bot.get_channel(Channel)  # 這裡替換成你的頻道 ID
                    targetMessage = await channel.fetch_message(Message)  # 這裡替換成你要刪除的訊息 ID

                    await targetMessage.delete()
                    print(f'{targetMessage.guild}_{targetMessage.channel} | {targetMessage.author}: {targetMessage.content} -> removed')
                    if call.guild:
                        await call.delete()
                    else:
                        await call.add_reaction('👌')
                except:
                    pass

token = os.environ.get('DISCORD_BOT_TOKEN')

if token is None:
    print(token)
else:
    bot.run(token)

import discord, os, json
from discord.ext import commands
from random import randrange
from pathlib import Path

intents = discord.Intents.default()
intents.dm_messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


def load(path):
    with open(path, 'r', encoding = 'utf8') as f:
        return json.load(f)

async def responder(m):
    dictPath = Path('C:\\Users\\jtn91\\OneDrive\\桌面\\Piyan\\Data\\reply_dictionary', f'{m.guild.id}/dictionary.json')
    try:
        return (load(dictPath)).get(m.content)[0]
    except:
        return None

async def mentionLot(m, times):
    for i in range(times):
        await m.channel.send(m.author.mention)
    await m.channel.send('很愛標?')

async def mentionBot(m, ans):
    try:
        if int(ans) == 1:
            await mentionLot(m, 5)
    except:
        await m.channel.send(ans)

@bot.event
async def on_message(m):
    if m.author.bot or not m.guild:
        return
    
    if '<@1043082295764078652>' in m.content: # 被標記
        VIP = load(Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/VIP/VIP.json'))
        call = m.content.split('1043082295764078652>')[1].strip().split(' ')[0]

        commands_list = load(Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/command_list/command_list.json'))
        piyanText = load(Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/command_list/reply_text.json'))
        call_list = commands_list + list(piyanText.keys())

        if call in call_list: # piyanCall 不在這
            return
        elif m.author.id in VIP:    # VIP 低聲下氣
            await m.channel.send('怎麼ㄌ')
        else:   # 非VIP 抽獎模式
            ans = load(Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/mention_ans/mention_ans.json'))
            await mentionBot(m, ans[randrange(len(ans))])
    elif "標我" in m.content:   # 沒啥用
        await m.reply(f"{m.author.mention} 標你了")
    elif await responder(m):    # 字典回覆
        await m.reply(await responder(m))

token = os.environ.get('DISCORD_BOT_TOKEN')

if token is None:
    print(token)
else:
    bot.run(token)

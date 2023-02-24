import discord, os, json, subprocess
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

def dump(data, path):
    with open(path, 'w', encoding = 'utf8') as f:
        json.dump(data, f, ensure_ascii=False)

wli = load(Path('wli/wli.json'))
cantSet = load(Path('cantSet/cantSet.json'))

async def responder(m):
    dictPath = Path('dict/dict.json')
    try:
        return (load(dictPath)).get(m.content)[0]
    except:
        return None

async def piyanCall(m, call):
    if call == '++':
        w = m.content.split()
        i = w.index('++')
        try:
            trigger, response = w[i+1], w[i+2]
        except:
            return None
        cantSet = load(Path('cantSet/cantSet.json'))
        if trigger in cantSet:
            print(m.author, 'cantSet', trigger)
            return '笑死 還想改啊'
        
        dictPath = Path('dict', 'dict.json')
        dictionary = load(dictPath)

        dictionary[trigger] = [response, f'{m.author}']
        dump(dictionary, dictPath)

        with open("dict\\dict.txt", "w", encoding='utf-8') as f:
            f.write(str(load("dict\\dict.json")).replace('{', '{\n').replace('}', '\n}').replace('], ', '], \n'))
        print(f'{m.author}({m.author.id}):\t {trigger} >>> {response}')
        return f'好ㄌ:\t{trigger} >>> {response}'
    return None

@bot.event
async def on_message(m):
    if m.author.bot:
        return
    
    if '<@1043082295764078652>' in m.content:
        call = m.content.split('1043082295764078652>')[1].strip().split(' ')[0]
        pyCall = await piyanCall(m, call)
        if pyCall:
            await m.channel.send(pyCall)
        elif m.author.id in wli:
            await m.channel.send('怎麼ㄌ')
        else:
            ans = ['沒事不要標我低能兒', '老子不是聊天機器人', '幹嘛', '有啥毛病', f'{m.author.mention}?', '怎麼ㄌ']
            await m.channel.send(ans[randrange(len(ans))])
    elif m.content.startswith("標我"):
        await m.channel.send(f"{m.author.mention}標你了")
    elif await responder(m):
        await m.reply(await responder(m))

token = os.environ.get('DISCORD_BOT_TOKEN')

if token is None:
    print(token)
else:
    bot.run(token)

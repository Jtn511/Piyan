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


async def piyanAdd(m):
    pattern = r"\+\+\s*(\S+)\s*(\S+)"
    match = re.search(pattern, m.content)   # 搜尋符合正規表達式的字串

    if match:   # 如果找到符合的字串，從捕捉群組中取得結果
        trigger = match.group(1)
        if trigger in load(Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/cantSet/cantSet.json')):
            print(m.author, 'cantSet', trigger)
            return '笑死 還想改啊'  # cannot set ㄏㄏ
        response = match.group(2)
    
    dictPath = Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/reply_dictionary', f'{m.guild.id}/dictionary.json')
    dictPath.parent.mkdir(parents=True, exist_ok=True)

    try:
        dictionary = load(dictPath)
    except:
        dictionary = {}

    dictionary[trigger] = [response, f'{m.author}', f'{m.author.id}']
    dump(dictionary, dictPath)

    dicTxt = Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/reply_dictionary', f'{m.guild.id}/recovery.txt')
    dicTxt.parent.mkdir(parents=True, exist_ok=True)

    with open(dicTxt, "w", encoding='utf-8') as f:    # 備份
        f.write(str(load(dictPath)).replace('{', '{\n').replace('}', '\n}').replace('], ', '], \n'))

    print(f'{m.author}:\t {trigger} >>> {response}')
    return f'好ㄌ:\t{trigger} >>> {response}'   # 成功

@bot.event
async def on_message(m):
    if m.author.bot:
        return
    
    if '<@1043082295764078652>' in m.content:
        if m.content.split('>')[1].strip().split(' ')[0] == "++":
            await m.channel.send(await piyanAdd(m))

token = os.environ.get('DISCORD_BOT_TOKEN')

if token is None:
    print(token)
else:
    bot.run(token)

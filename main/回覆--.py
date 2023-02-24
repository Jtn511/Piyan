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

async def piyanRemove(m):
    pattern = r"\-\-\s*(\S+)"
    match = re.search(pattern, m.content)   # 搜尋符合正規表達式的字串

    if match:   # 如果找到符合的字串，從捕捉群組中取得結果
        trigger = match.group(1)
        dictPath = Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/reply_dictionary', f'{m.guild.id}/dictionary.json')
        try:
            dictionary = load(dictPath)
            authorName = dictionary.get(trigger)[1]
            authorID = int(dictionary.get(trigger)[2])
            if m.author.id != authorID:   # 作者不符
                print(f'{m.author} cannot remove {trigger} from {authorName}')
                return '笑死 還想刪啊'
        except: # 沒檔案
            return '沒東西阿 你是要刪啥'

    del dictionary[trigger]
    dump(dictionary, dictPath)

    dicTxt = Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/reply_dictionary', f'{m.guild.id}/recovery.txt')
    dicTxt.parent.mkdir(parents=True, exist_ok=True)

    with open(dicTxt, "w", encoding='utf-8') as f:    # 備份
        f.write(str(load(dictPath)).replace('{', '{\n').replace('}', '\n}').replace('], ', '], \n'))

    print(f'{m.author}:\t {trigger} >>> None')
    return f'好ㄌ:\t\"{trigger}\" 現在跟我打的電話一樣 都是無回應'   # 成功


@bot.event
async def on_message(m):
    if m.author.bot:
        return
    
    if '<@1043082295764078652>' in m.content:
        if m.content.split('>')[1].strip().split(' ')[0] == "--":
            await m.channel.send(await piyanRemove(m))

token = os.environ.get('DISCORD_BOT_TOKEN')

if token is None:
    print(token)
else:
    bot.run(token)

import json, discord
from pathlib import Path
from discord import app_commands
from discord.ext import commands
from datetime import datetime
import requests

def load(path):
    if not path.exists():
        path.touch()
    with open(path, 'r', encoding = 'utf8') as f:
        return json.load(f)

def dump(data, path):
    with open(path, 'w', encoding = 'utf8') as f:
        json.dump(data, f, ensure_ascii=False)
    return

def add_reply(interaction, key, reply):
    cant_add_list = load(Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/cant_add/cant_add.json'))
    if key in cant_add_list:
        return '笑死 還想改啊'
    dictPath = Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/reply_dictionary', f'{interaction.guild.id}/dictionary.json')
    dictPath.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        dictionary = load(dictPath)
    except:
        dictionary = {}

    dictionary[key] = [reply, f'{interaction.user}', interaction.user.id]
    dump(dictionary, dictPath)

    dicTxt = Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/reply_dictionary', f'{interaction.guild.id}/{interaction.guild.name}.txt')
    dicTxt.parent.mkdir(parents=True, exist_ok=True)

    with open(dicTxt, "w", encoding='utf-8') as f:    # 備份
        f.write(str(load(dictPath)).replace('{', '{\n').replace('}', '\n}').replace('], ', '], \n'))

    return f'好ㄌ {key} >>> {reply}'

def remove_reply(interaction, key):
    VIP = load(Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/VIP/VIP.json'))
    dictPath = Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/reply_dictionary', f'{interaction.guild.id}/dictionary.json')
    try:
        dictionary = load(dictPath)
        reply, authorName, authorID = dictionary.get(key)
        if interaction.user.id not in VIP:
            if interaction.user.id != authorID:   # 作者不符
                print(f'{interaction.user} cannot remove {key} from {authorName}')
                return '笑死 還想刪啊'
    except TypeError: # 沒檔案
        return '沒東西阿 你是要刪啥'
    
    del dictionary[key]
    dump(dictionary, dictPath)
    dicTxt = Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/reply_dictionary', f'{interaction.guild.id}/{interaction.guild.name}.txt')
    dicTxt.parent.mkdir(parents=True, exist_ok=True)

    with open(dicTxt, "w", encoding='utf-8') as f:    # 備份
        f.write(str(load(dictPath)).replace('{', '{\n').replace('}', '\n}').replace('], ', '], \n'))
    print(f'{interaction.user}:\t {key} >>> None')

    return f"好ㄌ:\t現在 {key} 跟我打的電話一樣無回應"

def key_list(interaction):

    dictPath = Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/reply_dictionary', f'{interaction.guild.id}/dictionary.json')
    dictPath.parent.mkdir(parents=True, exist_ok=True)

    try: dictionary = load(dictPath)
    except: dictionary = {}

    replyKey = ""
    #replyValue = ""
    t = 5
    for i in dictionary:
        if t:
            replyKey += f"{i}\n"
            #replyValue += f"{dictionary[i][0][:15]}\n"

    embedVar = discord.Embed(title="Piyan List", color=0x4c9ce0)
    embedVar.add_field(name="關鍵字", value=replyKey, inline=True)
    #embedVar.add_field(name="回傳值", value=replyValue, inline=True)

    return embedVar

def reply(message):
    dictPath = Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/reply_dictionary', f'{message.guild.id}/dictionary.json')
    try:
        return (load(dictPath)).get(message.content)[0]
    except:
        return None
    
async def record_dm(message):
    if isinstance(message.channel, discord.DMChannel):
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

def responder(m):
    dictPath = Path('C:\\Users\\jtn91\\OneDrive\\桌面\\Piyan\\Data\\reply_dictionary', f'{m.guild.id}/dictionary.json')
    try:
        return (load(dictPath)).get(m.content)[0]
    except:
        return None
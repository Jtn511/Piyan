import json, discord
from pathlib import Path
from discord import app_commands
from discord.ext import commands

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
    except Exception as e: # 沒檔案
        print(e)
        return '沒東西阿 你是要刪啥'
    
    del dictionary[key]
    dump(dictionary, dictPath)
    dicTxt = Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/reply_dictionary', f'{interaction.guild.id}/recovery.txt')
    dicTxt.parent.mkdir(parents=True, exist_ok=True)

    with open(dicTxt, "w", encoding='utf-8') as f:    # 備份
        f.write(str(load(dictPath)).replace('{', '{\n').replace('}', '\n}').replace('], ', '], \n'))
    print(f'{interaction.user}:\t {key} >>> None')

    return f"好ㄌ:\t\"{key}\" 現在跟我打的電話一樣 都是無回應"

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
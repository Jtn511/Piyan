import json, discord, requests
from pathlib import Path
from discord import app_commands
from discord.ext import commands
from datetime import datetime
from random import randrange

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
    black_list = load(Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/member_list/black_list.json'))
    if key in cant_add_list:
        print(f'{interaction.user.name} cannot add {key} to {reply}')
        return '笑死 還想改啊'
    if interaction.user.id in black_list:
        print(f'{interaction.user.name} cannot add {key} to {reply} (black list)')
        return '李家豐鎖黑名單'
    dictPath = Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/guild_data', f'{interaction.guild.id}/dictionary.json')
    dictPath.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        dictionary = load(dictPath)
    except:
        dictionary = {}

    dictionary[key] = [reply, f'{interaction.user}', interaction.user.id]
    dump(dictionary, dictPath)

    dicTxt = Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/guild_data', f'{interaction.guild.id}/{interaction.guild.name}.txt')
    dicTxt.parent.mkdir(parents=True, exist_ok=True)

    with open(dicTxt, "w", encoding='utf-8') as f:    # 備份
        f.write(str(load(dictPath)).replace('{', '{\n').replace('}', '\n}').replace('], ', '], \n'))

    return f'好ㄌ:\t{key} >>> {reply}'

def remove_reply(interaction, key):
    VIP = load(Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/member_list/VIP.json'))
    dictPath = Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/guild_data', f'{interaction.guild.id}/dictionary.json')
    try:
        dictionary = load(dictPath)
        try:
            reply, authorName, authorID = dictionary.get(key)
        except ValueError:
            return '笑死 還想刪啊'
        if interaction.user.id not in VIP:
            if interaction.user.id != authorID:   # 作者不符
                print(f'{interaction.user} cannot remove {key} from {authorName}')
                return '笑死 還想刪啊'
    except TypeError: # 沒檔案
        return '沒東西阿 你是要刪啥'
    
    del dictionary[key]
    dump(dictionary, dictPath)
    dicTxt = Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/guild_data', f'{interaction.guild.id}/{interaction.guild.name}.txt')
    dicTxt.parent.mkdir(parents=True, exist_ok=True)

    with open(dicTxt, "w", encoding='utf-8') as f:    # 備份
        f.write(str(load(dictPath)).replace('{', '{\n').replace('}', '\n}').replace('], ', '], \n'))
    print(f'{interaction.user}:\t {key} >>> None')

    return f"好ㄌ:\t現在 {key} 跟我打的電話一樣無回應"

def author_search(interaction, key):
    dictPath = Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/guild_data', f'{interaction.guild.id}/dictionary.json')
    try:
        dictionary = load(dictPath)
        try:
            reply, authorName, authorID = dictionary.get(key)
            return f'**{key}** 是 <@{authorID}> 設的ㄏㄏ'
        except ValueError:
            return '這太早了 我沒記到設定者'
    except TypeError: # 沒檔案
        return '沒東西阿 你是要查啥'

def key_list(interaction):

    dictPath = Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/guild_data', f'{interaction.guild.id}/dictionary.json')
    dictPath.parent.mkdir(parents=True, exist_ok=True)

    try: dictionary = load(dictPath)
    except: dictionary = {}

    replyKey = ""
    #replyValue = ""
    num = ""
    t = 0
    for i in dictionary:
        t += 1
        num += f'{t}\n'
        replyKey += f"{i}\n"
        #replyValue += f"{dictionary[i][0][:15]}\n"

    embedVar = discord.Embed(title="Piyan List", color=0x4c9ce0)
    embedVar.add_field(name="No.", value=num, inline=True)
    embedVar.add_field(name="關鍵字", value=replyKey, inline=True)
    #embedVar.add_field(name="回傳值", value=replyValue, inline=True)

    return embedVar

def mentioned_reply(message):
    if message.author.id in VIP:    # VIP 低聲下氣
        ans = load(Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/mention_ans/mention_VIP.json'))
        message.reply(ans[randrange(len(ans))])
    else:   # 非VIP 抽獎模式
        ans = load(Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/mention_ans/mention_ans.json'))
        mentionBot(message, ans[randrange(len(ans))])

async def record_dm(message):
    if isinstance(message.channel, discord.DMChannel) and message.author.id != 1043082295764078652:
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
        f.write(f"{t} | {message.author}: {message.content}".replace('\n', f'\n                    | {message.author}: ')+"\n")
    return

def responder(m):
    dictPath = Path('C:\\Users\\jtn91\\OneDrive\\桌面\\Piyan\\Data\\guild_data', f'{m.guild.id}/dictionary.json')
    try:
        return (load(dictPath)).get(m.content)[0]
    except:
        return None
    
def say(interaction, text):
    say_path = Path(f'C:/Users/jtn91/OneDrive/桌面/Piyan/Data/guild_data/{interaction.guild.id}/say.txt')
    say_path.parent.mkdir(parents=True, exist_ok=True)
    t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(say_path, 'a', encoding='utf-8') as f:
        f.write(f"{t} | p5yan | {interaction.user}: {text}\n")
    return

def VIP(vip_list):
    vip_path = Path(f'C:/Users/jtn91/OneDrive/桌面/Piyan/Data/member_list/{vip_list}.json')
    return load(vip_path)

def create_embed():
# 建立embed物件
    embed = discord.Embed(
        title='皮炎公告',
        description='沒啥 純粹試試看',
        color=discord.Color.blue(), # 顏色
        url='https://www.google.com/', # 嵌入連結
    )

    # 增加作者
    embed.set_author(
        name='Piyan#0765',
        url='https://discord.com/api/oauth2/authorize?client_id=1043082295764078652&permissions=8&scope=bot',
        icon_url='https://imgur.com/46ScKGF.jpg'
    )

    # 增加縮圖
    embed.set_thumbnail(
        url='https://imgur.com/9f3yb2j.jpg'
    )
    
    # 增加欄位
    embed.add_field(
        name='欄位標題',
        value='欄位內容',
        inline=True # 是否為行內欄位
    )

    # 增加圖片
    embed.set_image(
        url='https://imgur.com/akGEDC0.jpg'
    )

    # 增加尾註
    embed.set_footer(
        text='--Piyan',
        icon_url='https://imgur.com/KiT5Wbh.jpg'
    )

    # 增加時間戳記
    embed.timestamp = datetime.datetime.now()

    return embed

def amount_search(guildID, author):
    dictPath = Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/guild_data', f'{guildID}/dictionary.json')
    dict = load(dictPath)
    amount = 0
    for key in dict:
        try:
            if dict[key][2] == author.id:
                amount += 1
        except:
            dict[key] += ['', '']

    return f'{author.mention}在piyan裡面設了 {amount} 次'

def avatar_delete(message):
    avatar = VIP('avatar')
    if message.author.id == 172002275412279296:
        return 1
    try:
        for mem in avatar:
            if f'{mem}' in f'{message.embeds[0].to_dict()}':
                return 1
    except IndexError:
        return None

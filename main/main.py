import discord, os, Piyan
from discord import app_commands
from discord.ext import commands
from Piyan import load, Path, datetime
from random import randrange

bot = commands.Bot(command_prefix='!', intents= discord.Intents.all())

async def mentionLot(m, times):
    for i in range(times):
        await m.channel.send(m.author.mention)
    await m.reply('很愛標?')

async def mentionBot(m, ans):
    try:
        if int(ans) == 1:
            await mentionLot(m, 5)
    except:
        await m.channel.send(ans)

@bot.event
async def on_ready():
    print('\nPiyan已啟動!', end='\t')
    try:
        synced = await bot.tree.sync()
        print(f'現在有 {len(synced)} 個指令!')
        for i in range(len(synced)):
            print(synced[i].name)
    except Exception as e:
        print(e)

@bot.event
async def on_message(message):
    if message.guild:
        await Piyan.record_guild(message)
    else:
        await Piyan.record_dm(message)
    
    if message.type.value == 20:
        if Piyan.avatar_delete(message):
            await message.delete()
    if message.author.bot or not message.guild:
        return
    
    VIP = load(Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/member_list/VIP.json'))
    if str(bot.user.id) in message.content: # 被標記
        if message.author.id in VIP:    # VIP 低聲下氣
            ans = load(Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/mention_ans/mention_VIP.json'))
            await message.reply(ans[randrange(len(ans))])
        else:   # 非VIP 抽獎模式
            ans = load(Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/mention_ans/mention_ans.json'))
            await mentionBot(message, ans[randrange(len(ans))])
    elif "標我" in message.content:   # 沒啥用
        await message.reply(f"{message.author.mention} 標你了")
    elif Piyan.responder(message):    # 字典回覆
        await message.reply(Piyan.responder(message))
        
@bot.event
async def on_raw_reaction_add(reaction):
    if reaction.emoji.name == '👾' and reaction.member.id in Piyan.VIP('VIP'):
        channel = bot.get_channel(reaction.channel_id)  # 這裡替換成你的頻道 ID
        message = await channel.fetch_message(reaction.message_id)  # 這裡替換成你要刪除的訊息 ID

        await message.delete()
        print(f'{message.guild}_{message.channel} | {message.author}: {message.content} -> removed by {reaction.member}')


@bot.tree.command(name='p0yan功能', description='查看Piyan的功能列表')
async def piyan(interaction: discord.Interaction):
    await interaction.response.send_message(f'還沒寫 先假裝這是列表')


@bot.tree.command(name='p1yan測試', description='點一下不吃虧啊')
async def test(interaction: discord.Interaction):
    await interaction.response.send_message(f'{interaction.user.mention} 的屁演很新鮮，請安心使用。')


@bot.tree.command(name='p2yan回覆十十', description='新增你的回覆')
@app_commands.describe(key= '輸入你要加的關鍵字', reply= '回覆內容')
async def add_reply(interaction: discord.Interaction, key: str, reply: str):
    await interaction.response.send_message(Piyan.add_reply(interaction, key, reply))


@bot.tree.command(name='p3yan回覆一一', description='刪除你的回覆')
@app_commands.describe(key= '輸入你要刪的關鍵字')
async def remove_reply(interaction: discord.Interaction, key: str):
    await interaction.response.send_message(Piyan.remove_reply(interaction, key))


@bot.tree.command(name='p4yan查設定人', description='看看是哪個王八蛋設的')
@app_commands.describe(key= '輸入你要查的關鍵字')
async def author_search(interaction: discord.Interaction, key: str):
    await interaction.response.send_message(Piyan.author_search(interaction, key))


@bot.tree.command(name='p5yan查數量', description='看看他到底設了多少')
@app_commands.describe(author= '輸入你要查的關鍵字')
async def amount_search(interaction: discord.Interaction, author: discord.Member):
    await interaction.response.send_message(Piyan.amount_search(interaction.guild.id, author))


@bot.tree.command(name='p6yan關鍵字清單', description='太多了所以不想放回覆內容 好奇的自己試試就知道了')
async def list(interaction: discord.Interaction):
    try:
        await interaction.response.send_message(embed=Piyan.key_list(interaction), ephemeral=True)
    except:
        await interaction.response.send_message('字太多了我還沒寫解決方案ㄟ', ephemeral=True)


@bot.tree.command(name='p7yan轟炸機', description='五次轟炸尋人機')
@app_commands.describe(target= '炸誰?', text= '轟炸內容?')
async def bomb(interaction: discord.Interaction, target: discord.Member, text: str):
    await interaction.response.send_message(f'{interaction.user.mention} 對 {target.mention} 使用轟炸')
    for i in range(5):
        await interaction.channel.send(f'{target.mention} {text}')
    await interaction.channel.send('你家炸了 快出來')


@bot.tree.command(name='p8yan代言人', description='幫你大聲說出來!')
@app_commands.describe(say= '講出來')
async def say(interaction: discord.Interaction, say: str):
    Piyan.say(interaction, say)
    await interaction.channel.send(say)
    await interaction.response.send_message('俗辣不敢自己講喔', ephemeral= True)


token = os.getenv('DISCORD_BOT_TOKEN')
bot.run(token)
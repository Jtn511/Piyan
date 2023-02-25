import discord, os, Piyan
from discord import app_commands
from discord.ext import commands
from Piyan import load, Path
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
    except Exception as e:
        print(e)

@bot.event
async def on_message(message):
    if message.guild:
        await Piyan.record_guild(message)
    else:
        await Piyan.record_dm(message)
        
    if message.author.bot or not message.guild:
        return
    
    VIP = load(Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/VIP/VIP.json'))
    if '<@1043082295764078652>' in message.content: # 被標記
        if message.author.id in VIP:    # VIP 低聲下氣
            ans = ['怎麼ㄌ', '老大請說', '主人，我在']
            await message.reply(ans[randrange(len(ans))])
        else:   # 非VIP 抽獎模式
            ans = load(Path('C:/Users/jtn91/OneDrive/桌面/Piyan/Data/mention_ans/mention_ans.json'))
            await mentionBot(message, ans[randrange(len(ans))])
    elif "標我" in message.content:   # 沒啥用
        await message.reply(f"{message.author.mention} 標你了")
    elif Piyan.responder(message):    # 字典回覆
        await message.reply(Piyan.responder(message))
        
        
        
        
        
        
        
        
        
        
        
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


@bot.tree.command(name='p4yan關鍵字清單', description='太多了所以不想放回覆內容 好奇的自己試試就知道了')
async def list(interaction: discord.Interaction):
    try:
        await interaction.response.send_message(embed=Piyan.key_list(interaction), ephemeral=True)
    except:
        await interaction.response.send_message('字太多了我還沒寫解決方案ㄟ')










token = os.getenv('DISCORD_BOT_TOKEN')
bot.run(token)
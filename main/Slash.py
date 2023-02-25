import discord, os
from discord import app_commands
from discord.ext import commands
import Piyan

bot = commands.Bot(command_prefix='!', intents= discord.Intents.all())

@bot.event
async def on_ready():
    print('\nPiyan已啟動!')
    try:
        synced = await bot.tree.sync()
        print(f'現在有 {len(synced)} 個指令!')
    except Exception as e:
        print(e)


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
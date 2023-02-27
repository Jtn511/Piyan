import discord, os, datetime

client = discord.Client(intents=discord.Intents.all())
token = "MTA3OTMzOTIzNDkwMjY4MzY3OA.GLpdvd.N9zzYeV3wjwn-rfdQWGYUxEWFpkQ1aibN-V1Ew"

@client.event
async def on_ready():

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

    for guild in client.guilds:
        if guild.name == '屁眼派對':
            for channel in guild.channels:
                if channel.name == '屁眼測試區':
                    await channel.send(embed=embed)



TOKEN = os.getenv('DISCORD_BOT_TOKEN')
client.run(TOKEN)

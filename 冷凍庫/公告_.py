import discord, os, datetime

client = discord.Client(intents=discord.Intents.all())
token = "MTA3OTMzOTIzNDkwMjY4MzY3OA.GhtkGh.nF20DL7ZiKDk4jf8pAG-8EeVzru1XAnOzzs7WI"

import discord
from discord.ext import commands
from discord.components import DiscordComponents, Button, ButtonStyle, InteractionType

bot = commands.Bot(command_prefix='!')
DiscordComponents(bot)

@bot.command()
async def embed(ctx):
    embed1 = discord.Embed(title='Page 1', description='This is page 1')
    embed2 = discord.Embed(title='Page 2', description='This is page 2')
    embed3 = discord.Embed(title='Page 3', description='This is page 3')

    pages = [embed1, embed2, embed3]
    current_page = 0

    message = await ctx.send(embed=pages[current_page], components=[[
        Button(style=ButtonStyle.blue, label='Previous', emoji='⬅️'),
        Button(style=ButtonStyle.blue, label='Next', emoji='➡️'),
    ]])

    while True:
        try:
            interaction = await bot.wait_for('button_click', timeout=30.0)
            if interaction.message.id != message.id:
                # 如果不是這個訊息的按鈕被點擊了，忽略
                continue
            if interaction.author.id != ctx.author.id:
                # 如果不是這個命令的執行者點擊了按鈕，忽略
                await interaction.respond(type=InteractionType.ChannelMessageWithSource, content='Sorry, only the command author can use this button.')
                continue

            if interaction.component.label == 'Next':
                current_page += 1
                if current_page >= len(pages):
                    current_page = 0
                await interaction.respond(type=InteractionType.UpdateMessage, embed=pages[current_page])
            elif interaction.component.label == 'Previous':
                current_page -= 1
                if current_page < 0:
                    current_page = len(pages) - 1
                await interaction.respond(type=InteractionType.UpdateMessage, embed=pages[current_page])
        except TimeoutError:
            await message.edit(components=None)
            break




TOKEN = os.getenv('DISCORD_BOT_TOKEN')
client.run(TOKEN)

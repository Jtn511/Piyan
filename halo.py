import discord
import os

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print('Bot is ready.')

@client.event
async def on_message(message):
    if message.content == 'send pic':
        
        with open('announcement.png', 'rb') as f:
            await message.channel.send(file=discord.File(f))

client.run(os.getenv('DISCORD_BOT_TOKEN'))

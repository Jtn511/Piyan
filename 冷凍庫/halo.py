import discord

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_message(message):
    try:
        print('---------------------------------')
        if message.interaction.name == 'avatar':
            await message.delete()
            print('avatar deleted')
        print('--------------------------------')
    except Exception as e:
        print(e)
        print('---------------------------------\n')
    exit()

TOKEN = 'MTA3OTMzOTIzNDkwMjY4MzY3OA.Gbmj6X.1zpZU3lK9ln8oNlJEFw8BrwTi7FbBoS30aZvZs'
client.run(TOKEN)

import os
import discord
import openai
from dotenv import load_dotenv

load_dotenv() # 載入環境變數

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GPT_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = GPT_API_KEY

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} 已上線！')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!chat '):
        # 從用戶消息中提取文本
        text = message.content[6:]
        
        # 使用 ChatGPT 生成回覆消息
        response = openai.Completion.create(
            engine="davinci", prompt=text, max_tokens=1024, n=1, stop=None, temperature=0.5,
        )

        # 將 ChatGPT 回覆消息發送回用戶
        await message.channel.send(response.choices[0].text)
    
client.run(TOKEN)

# 以上程式使用 dotenv 模組載入環境變數，包括 Discord Bot 的令牌（DISCORD_TOKEN）和 OpenAI 的 API 金鑰（OPENAI_API_KEY）。當 Discord Bot 收到消息時，它會檢查消息是否以 !chat 開頭，如果是，則使用 ChatGPT 生成回覆消息，並將其發送回用戶。

# 請確保你已安裝 discord.py，openai 和 dotenv 模組。你需要在 .env 文件中定義 DISCORD_TOKEN 和 OPENAI_API_KEY 環境變數。
import os
import discord
import openai
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv() # 載入環境變數

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GPT_API_KEY = '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'
openai.api_key = GPT_API_KEY
intent = discord.Intents.default()
intent.message_content = True

bot = commands.Bot(command_prefix='!', intents=intent)

@bot.event
async def on_ready():
    print(f'{bot.user} 已上線！')

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    print(message.content)
    if message.content.startswith('!chat '):
        # 從用戶消息中提取文本
        text = message.content[6:]
        print(text)
        # 使用 ChatGPT 生成回覆消息
        response = openai.Completion.create(
            engine="davinci", prompt=text, max_tokens=1024, n=1, stop=None, temperature=0.5,
        )
        print('response', response)
        # 將 ChatGPT 回覆消息發送回用戶
        if len(response.choices[0].text) > 2000:
        # 如果回复的文本长度超过了限制，进行截断或者提示用户
            truncated_text = response.choices[0].text[:1997] + "..."
            await message.channel.send("对不起，我的回复太长了！\n" + truncated_text)
        else:
            await message.reply(response.choices[0].text)


    
bot.run(TOKEN)

# 以上程式使用 dotenv 模組載入環境變數，包括 Discord Bot 的令牌（DISCORD_TOKEN）和 OpenAI 的 API 金鑰（OPENAI_API_KEY）。當 Discord Bot 收到消息時，它會檢查消息是否以 !chat 開頭，如果是，則使用 ChatGPT 生成回覆消息，並將其發送回用戶。

# 請確保你已安裝 discord.py，openai 和 dotenv 模組。你需要在 .env 文件中定義 DISCORD_TOKEN 和 OPENAI_API_KEY 環境變數。

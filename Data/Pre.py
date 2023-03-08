from pypresence import Presence # Presence 客戶端
import time, os                     # 等一下這也會用到

token = os.getenv("DISCORD_BOT_TOKEN")
presenceClient = Presence(client_id = token)

client.connect()
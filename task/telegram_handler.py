from telethon import TelegramClient
from app import send_webhook
from dotenv import load_dotenv
import os


load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
db_link = os.getenv("DB_LINK")

client = TelegramClient(...)

@client.on(events.NewMessage)
async def handler(event):
   # обработка 
   await send_webhook(event)

client.run_until_disconnected()
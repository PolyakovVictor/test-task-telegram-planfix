import telethon
from dotenv import load_dotenv
from flask import Flask, jsonify, request
import os
from uuid import uuid4
import asyncio
from telethon import TelegramClient, events


app = Flask(__name__)
load_dotenv()
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

session_folder = 'test_sessions'
if not os.path.exists(session_folder):
    os.makedirs(session_folder)

session_token = str(uuid4())


session_name = f'{session_folder}/session_{session_token}'

bot = TelegramClient(session_name, api_id=api_id, api_hash=api_hash).start(bot_token=bot_token)



@bot.on(events.NewMessage())
async def start(event):
    await event.respond('hello')
    bot.disconnect()


def main():
    bot.run_until_disconnected()


if __name__ == "__main__":
    main()

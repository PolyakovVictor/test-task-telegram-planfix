import telethon
from dotenv import load_dotenv
from telethon import TelegramClient
from flask import Flask, jsonify, request
from telethon.errors import SessionPasswordNeededError
import os
from uuid import uuid4
from telethon.sessions import StringSession


app = Flask(__name__)
load_dotenv()
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
session_folder = 'sessions'
if not os.path.exists(session_folder):
    os.makedirs(session_folder)


client = TelegramClient(
    f"{session_folder}/session_test",
    api_id,
    api_hash,
    bot_token=bot_token
).start(bot_token=bot_token)

# check status
status = "online" if client.is_connected() else "offline"


if __name__ == "__main__":
    app.run()

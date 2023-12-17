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
phone = 380665610258
session_folder = 'test_sessions'
if not os.path.exists(session_folder):
    os.makedirs(session_folder)

session_token = str(uuid4())

path = f"{session_folder}/sessing_{session_token}",

client = TelegramClient('session', api_id=api_id, api_hash=api_hash)

client.start(bot_token=bot_token)


client.session.save()


# with TelegramClient(StringSession(), api_id, api_hash).start(bot_token=bot_token) as client:
#     print('\n\nBelow is your session string ⬇️\n\n')
#     print(client.session.save())
#     print('\nAbove is your session string ⬆️\n\n')

# check status
print('check status')
status = "online" if client.is_connected() else "offline"
print(status)


if __name__ == "__main__":
    app.run(debug=True)

import telethon
from dotenv import load_dotenv
from flask import Flask, jsonify, request
import os
import requests
import asyncio
from telethon import TelegramClient, events


app = Flask(__name__)
load_dotenv()
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

session_folder = 'sessions'
if not os.path.exists(session_folder):
    os.makedirs(session_folder)

# session_token = str(uuid4())
session_token = '5617bd24-14c4-4191-8a41-c39e1777b51d'


class TelegramBot:

    def __init__(self, session_path):
        self.api_url = "https://example.com/api" 
        self.client = TelegramClient(session_path, api_id, api_hash)

    async def forward_messages(self):
        @self.client.on(events.NewMessage)
        async def handler(event):
            message = event.raw_text
            print(message)
            response = requests.post(f"{self.api_url}/new_message", json={"message": message})
            print(response.status_code)

    async def send_message(self, chat_id, text):
        await self.client.start()
        await self.client.send_message(chat_id, text)

    async def run(self):
        asyncio.create_task(self.forward_messages())
        asyncio.create_task(self.send_message('daste21', 'blablabla'))
        await asyncio.Future()


async def main():

    bot = TelegramBot("sessions/session_9c1fe40a-611e-4956-b708-e94137842796.session")
    await bot.run()     # запуск в отдельном потоке

    bot2 = TelegramBot("sessions/session_9c1fe40a-611e-4956-b708-e94137842796.session")
    await bot2.send_message('daste21', 'blablabla')     # вызов с await

asyncio.run(main())

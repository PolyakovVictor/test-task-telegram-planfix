import telethon
from dotenv import load_dotenv
from flask import Flask, jsonify, request
import os
from uuid import uuid4
import asyncio
from telethon import TelegramClient


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


session_name = f'{session_folder}/session_{session_token}'


async def first_connect():

    client = TelegramClient(session_name, api_id, api_hash)
    await client.start()

    phone = '+79211234567'
    code = input('Введите код подтверждения: ')
    await client.auth(phone, code)

    print(client.is_connected())

    await client.disconnect()


async def reconnect():
    client = TelegramClient(f'{session_folder}/session_1e14c235-55b2-4e73-b070-edfb2b2a4371', api_id, api_hash)
    try:
        await client.connect()
        user = await client.get_input_entity('@daste21')
        await client.send_message(user, 'test message2')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        await client.disconnect()



# переписать все от имени бота с открытием сессии под бота
async def main():

    await reconnect()

if __name__ == '__main__':
    asyncio.run(main())

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

session_folder = 'test_sessions'
if not os.path.exists(session_folder):
    os.makedirs(session_folder)

session_token = str(uuid4())


session_name = f'{session_folder}/session_{session_token}'


async def first_connect():

    client = TelegramClient(session_name, api_id, api_hash)
    await client.start()

    phone = '+49211234567'
    code = input('Введите код подтверждения: ')
    await client.auth(phone, code)

    print(client.is_connected())

    await client.disconnect()


async def reconnect():
    client = TelegramClient('sessions/session_4c00f5e8-9872-4cac-9cdf-d28a11a873e1', api_id, api_hash)
    try:
        await client.connect()
        user = await client.get_input_entity('daste21')
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

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

path_session = 'sessions'
name_session = 'session'


async def check_path_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)


@app.route("/start", methods=["POST"])
async def start_telegram_client():
    data = request.json

    name = data.get("name")
    number = data.get("number")
    # name_session = data.get("name_session")
    # path_session = data.get("path_session")

    session_token = uuid4()

    # if not all([name_session, path_session]):
    #     path_session = 'sessions'
    #     name_session = f"session_{session_token}.session"
    #     await check_path_exist(path_session)

    await check_path_exist(path_session)

    client = TelegramClient(
        f"{path_session}/{name_session}_{session_token}",
        api_id,
        api_hash,
    )

    await client.start(bot_token=bot_token)

    status = "online" if client.is_connected() else "offline"

    session_path = f"{path_session}/{name_session}_{session_token}.session"
    if client.is_connected():
        session_string = StringSession.save(client.session)
        if session_string:
            with open(session_path, "wb") as file:
                file.write(session_string.encode('utf-8'))
                # Save name and number along with the session
                file.write(f"\nName: {name}\nNumber: {number}".encode('utf-8'))
        else:
            return jsonify({"error": "Session string is empty"}), 500
    else:
        return jsonify({"error": "Client is not connected"}), 500

    return {
        "name": name,
        "status": status,
        "token": session_token,
    }


@app.route("/start", methods=["GET"])
async def get_telegram_session_status():
    session_token = request.headers.get("Token")

    if not session_token:
        return "Token not provided", 401

    if not os.path.exists(f"sessions/session_{session_token}.session"):
        return "Session not found", 404

    client = TelegramClient(
        f"{path_session}/{name_session}_{session_token}",
        api_id,
        api_hash
    )

    await client.connect()

    if client.is_connected():
        status = "online"
    else:
        status = "offline"

    await client.disconnect()

    return {
        "status": status
    }


@app.route("/start", methods=["DELETE"])
async def stop_telegram_client():
    session_token = request.headers.get("Token")

    if not session_token:
        return "Token not required", 401

    if not os.path.exists(f"{path_session}/session_{session_token}.session"):
        return "Session not found", 404

    client = TelegramClient(
        f"{path_session}/session_{session_token}",
        api_id,
        api_hash
    )

    await client.connect()

    if not client.is_connected():
        return "Client is already disconnected", 400

    await client.disconnect()
    os.remove(f"{path_session}/session_{session_token}.session")

    return "Ok"

if __name__ == "__main__":
    app.run()

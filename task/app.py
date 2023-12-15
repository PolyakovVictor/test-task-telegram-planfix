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


@app.route("/start", methods=["POST"])
async def start_telegram_client():
    # Отримуємо дані для запуску клієнта
    data = request.json
    session_token = uuid4()

    # create telegram client
    client = TelegramClient(
        f"{session_folder}/session_{session_token}",
        api_id,
        api_hash,
    )

    await client.start(bot_token=bot_token)

    # check status
    status = "online" if client.is_connected() else "offline"
    print(status)

    session_path = f"{session_folder}/session_{session_token}.session"
    if client.is_connected():
        session_string = StringSession.save(client.session)
        if session_string:
            with open(session_path, "wb") as file:
                file.write(session_string.encode('utf-8'))
        else:
            return jsonify({"error": "Session string is empty"}), 500
    else:
        return jsonify({"error": "Client is not connected"}), 500

    return {
        "name": data["name"],
        "status": status,
        "token": session_token,
    }


@app.route("/start", methods=["GET"])
async def get_telegram_session_status():
    session_token = request.headers.get("Token")

    if not session_token:
        return "Token not provided", 401

    if not os.path.exists(f"{session_folder}/session_{session_token}.session"):
        return "Session not found", 404

    client = TelegramClient(
        f"{session_folder}/session_{session_token}",
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

    if not os.path.exists(f"{session_folder}/session_{session_token}.session"):
        return "Session not found", 404

    client = TelegramClient(
        f"{session_folder}/session_{session_token}",
        api_id,
        api_hash
    )

    await client.connect()

    if not client.is_connected():
        return "Client is already disconnected", 400

    await client.disconnect()
    os.remove(f"{session_folder}/session_{session_token}.session")

    return "Ok"

if __name__ == "__main__":
    app.run()

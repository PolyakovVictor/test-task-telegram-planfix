import telethon
from dotenv import load_dotenv
from telethon import TelegramClient
from flask import Flask, jsonify, request
from telethon.errors import SessionPasswordNeededError
import os
from uuid import uuid4
from telethon.sessions import StringSession
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
db_link = os.getenv("DB_LINK")

app.config['SQLALCHEMY_DATABASE_URI'] = db_link
db = SQLAlchemy(app)


path_session = 'sessions'
name_session = 'session'


class TelegramSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    number = db.Column(db.String(15))
    url_planfix = db.Column(db.String(100))
    token_planfix = db.Column(db.String(100))
    name_session = db.Column(db.String(50))
    path_session = db.Column(db.String(100))
    session_token = db.Column(db.Text)


with app.app_context():
    db.create_all()


async def check_path_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)


@app.route("/start", methods=["POST"])
async def start_telegram_client():
    data = request.json

    name = data.get("name")
    number = data.get("number")
    url_planfix = data.get("url_planfix")
    token_planfix = data.get("token_planfix")
    name_session = data.get("name_session")
    path_session = data.get("path_session")

    if not all((name_session, path_session)):
        name_session = 'session'
        path_session = 'sessions'

    session_token = str(uuid4())

    session_data = TelegramSession(
        name=name,
        number=number,
        url_planfix=url_planfix,
        token_planfix=token_planfix,
        name_session=name_session,
        path_session=path_session,
        session_token=session_token
    )

    await check_path_exist(path_session)

    client = TelegramClient(
        f"{path_session}/{name_session}_{session_token}",
        api_id,
        api_hash,
    )

    try:
        await client.start(bot_token=bot_token)
    except Exception as e:
        print(f'Error: {e}')

    status = "online" if client.is_connected() else "offline"

    if client.is_connected():
        client.disconnect()
        with app.app_context():  # Creating the app context
            db.session.add(session_data)
            db.session.commit()
    else:
        return jsonify({"error": "Client is not connected"}), 500

    return {
        "name": name,
        "status": status,
        "token": session_token,
    }


@app.route("/status", methods=["GET"])
async def get_status():
    session_token = request.headers.get("Token")

    if not session_token:
        return jsonify({"error": "Token is missing"}), 400

    session = TelegramSession.query.filter_by(session_token=session_token).first()

    if not session:
        return jsonify({"error": "Invalid token"}), 400

    path = os.path.join(session.path_session, f"{session.name_session}_{session_token}.session")

    client = TelegramClient(path, api_id, api_hash)

    try:
        await client.connect()
        status = "online" if client.is_connected() else "offline"
    except Exception as e:
        print(f'Error: {e}')
    finally:
        await client.disconnect()
    return jsonify({
        "status": status
    })


@app.route("/stop", methods=["DELETE"])
async def stop_telegram_client():
    session_token = request.headers.get("Token")

    if not session_token:
        return jsonify({"error": "Token is missing"}), 400

    # Using the same session throughout
    session = db.session

    obj = session.query(TelegramSession).filter_by(session_token=session_token).first()
    path = f"{obj.path_session}/{obj.name_session}_{session_token}.session"

    if not obj:
        return jsonify({"error": "Invalid token"}), 400

    if os.path.exists(path):  # Check if the file exists before attempting deletion
        try:
            os.remove(path)
        except Exception as e:
            return jsonify({"error": f"Failed to delete file: {str(e)}"}), 500
    else:
        return jsonify({"error": "File does not exist"}), 404

    with app.app_context():
        obj = session.merge(obj)
        session.delete(obj)
        session.commit()

    return jsonify({"status": "offline"})


if __name__ == "__main__":
    app.run(debug=True)

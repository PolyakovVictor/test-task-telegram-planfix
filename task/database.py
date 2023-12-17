from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import os
from dotenv import load_dotenv
from models import TelegramSession


load_dotenv()
db_link = os.getenv("DB_LINK")

async_engine = create_async_engine(
    url=db_link,
    echo=True
)

async_session = async_sessionmaker(async_engine)


async def create_telegram_session():
    async with async_session() as session:
        new_session = TelegramSession(
            name='name',
            number='number',
            url_planfix='url_planfix',
            token_planfix='token_planfix',
            name_session='name_session',
            path_session='path_session',
            session_token='session_token'
        )
        session.add(new_session)
        await session.commit()

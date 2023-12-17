from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class TelegramSession(Base):
    __tablename__ = 'telegram_sessions'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    number = Column(String(15))
    url_planfix = Column(String(100))
    token_planfix = Column(String(100))
    name_session = Column(String(50))
    path_session = Column(String(100))
    session_token = Column(Text)

from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy import create_engine, Column, String, Text, Integer, Boolean
from datetime import datetime
# Создаем базовый класс моделей
Base = declarative_base()

# Определяем модели


class BotActivity(Base):
    __tablename__ = 'bot_activity'
    chat_id = Column(String, primary_key=True)
    is_bot_active = Column(Boolean, default=False)


class UserNames(Base):
    __tablename__ = 'usernames'
    chat_id = Column(Integer, primary_key=True)
    username = Column(String, default='')
    name = Column(String, default='')


class AmoNewStages(Base):
    __tablename__ = 'amo_new_stages'
    chat_id = Column(Integer, primary_key=True)
    username = Column(String, default='')
    name = Column(String, default='')
    status_id = Column(String, default='')


class NewPrompt(Base):
    __tablename__ = 'new_prompt'
    chat_id = Column(Integer, primary_key=True)
    prompt = Column(Text, default='')


class Users(Base):
    __tablename__ = 'users'
    username = Column(String, primary_key=True)
    name = Column(String, default='')
    chat_id = Column(Integer, default=0)
    user_id = Column(String, default='')


class LeadId(Base):
    __tablename__ = 'lead_id'
    chat_id = Column(Integer, primary_key=True)
    lead_id = Column(String, default='')


class ShortedHistory(Base):
    __tablename__ = 'shorted_history'
    chat_id = Column(Integer, primary_key=True)
    history = Column(Text, default='')
    shorted_rows = Column(Integer)


class MessagesFromClient(Base):
    __tablename__ = 'messages_from_client'
    chat_id = Column(Integer, primary_key=True)
    message_united = Column(Text, default='')


class IsBotFree(Base):
    __tablename__ = 'is_bot_free'
    chat_id = Column(Integer, primary_key=True)
    is_bot_free = Column(Boolean, default=True)


class RecentMessages(Base):
    __tablename__ = 'recent_messages'
    chat_id = Column(Integer, primary_key=True)
    time = Column(DateTime, default=datetime.utcnow())
    stage_in_amo = Column(String, default='')


class ListOfNewMessages(Base):
    __tablename__ = 'new_messages_from_amo'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, default=None)
    new_message = Column(String, default=None)
    username = Column(String, default=None)
    name = Column(String, default=None)
    media_download_link = Column(String, default=None)
    file_name = Column(String, default=None)


class Analysis(Base):
    __tablename__ = 'analysis'
    chat_id = Column(Integer, primary_key=True)
    has_analysis = Column(Boolean, default=True)


class DealsToClose(Base):
    __tablename__ = 'deals_to_close'
    chat_id = Column(Integer, primary_key=True)
    count_to_close_deal = Column(Integer, default=0)

from datetime import datetime, timedelta
from aiogram.types import user
from sqlalchemy import create_engine, Column, String, Text, Integer, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
import random
import string
from sqlalchemy.sql.sqltypes import DateTime
import os
from dotenv import load_dotenv

load_dotenv()
username = str(os.getenv('USERNAME'))
password = str(os.getenv('PASSWORD'))
host = str(os.getenv('HOST'))
port = str(os.getenv('PORT'))
database = str(os.getenv('DATABASE'))

connection_string = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}'
engine = create_engine(connection_string)

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


def generate_random_string(length):
    letters = string.ascii_lowercase
    result = ''.join(random.choice(letters) for _ in range(length))
    return result


def generate_random_digits(length):
    letters = string.digits
    result = ''.join(random.choice(letters) for _ in range(length))
    return result


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def add_has_analysis(chat_id):
    new_addition = Analysis(
        chat_id=chat_id, has_analysis=True)
    session.merge(new_addition)
    session.commit()


def add_in_deal_to_close(chat_id, stage_close):
    new_addition = DealsToClose(
        chat_id=chat_id, count_to_close_deal=stage_close)
    session.merge(new_addition)
    session.commit()


def get_count_to_close(chat_id: int):
    user = session.query(DealsToClose).filter_by(chat_id=chat_id).first()
    if user:
        return user.count_to_close_deal
    else:
        return 0


def delete_count_to_close(chat_id: int):
    user = session.query(DealsToClose).filter_by(chat_id=chat_id).first()
    if user:
        session.delete(user)
        session.commit()
    else:
        return 0


def check_has_analysis(chat_id):
    user = session.query(Analysis).filter_by(chat_id=chat_id).first()
    if user:
        return user.has_analysis
    else:
        return False


def add_new_message(chat_id, new_message, username, name, media_link, file_name):
    try:
        new_addition = ListOfNewMessages(chat_id=chat_id, new_message=new_message,
                                         username=username, name=name, media_download_link=media_link, file_name=file_name)
        session.add(new_addition)
        session.commit()
        return True
    except:
        return False


def add_shorted_history(chat_id, shorted_history, shorted_rows: int):
    try:
        existing_entry = session.query(
            ShortedHistory).filter_by(chat_id=chat_id).first()
        if existing_entry:
            existing_entry.history += " " + shorted_history  # Дополняем существующий текст
            # Обновляем количество сокращенных строк
            existing_entry.shorted_rows = shorted_rows
        else:
            new_addition = ShortedHistory(
                chat_id=chat_id, history=shorted_history, shorted_rows=shorted_rows)
            session.add(new_addition)
        session.commit()
    except Exception as e:
        print(e)


def add_message_from_client(chat_id, message):
    try:
        existing_entry = session.query(
            MessagesFromClient).filter_by(chat_id=chat_id).first()
        if existing_entry:
            existing_entry.message_united += " " + message  # Дополняем существующий текст
        else:
            new_addition = MessagesFromClient(
                chat_id=chat_id, message_united=message)
            session.merge(new_addition)
        session.commit()
    except Exception as e:
        print(e)


def delete_shorted_history(chat_id: int):
    try:
        existing_entry = session.query(
            ShortedHistory).filter_by(chat_id=chat_id).first()
        if existing_entry:
            session.delete(existing_entry)
            session.commit()
        else:
            print(f"No row found with chat_id {chat_id}.")
    except Exception as e:
        print(e)


def delete_messages_from_client(chat_id: int):
    try:
        existing_entry = session.query(
            MessagesFromClient).filter_by(chat_id=chat_id).first()
        if existing_entry:
            session.delete(existing_entry)
            session.commit()
        else:
            print(f"No row found with chat_id {chat_id}.")
    except Exception as e:
        print(e)


def merge_shorted_history(chat_id, shorted_history, shorted_rows: int):
    try:
        existing_entry = session.query(
            ShortedHistory).filter_by(chat_id=chat_id).first()
        if existing_entry:
            existing_entry.history = shorted_history
            existing_entry.shorted_rows = shorted_rows
        else:
            new_addition = ShortedHistory(
                chat_id=chat_id, history=shorted_history, shorted_rows=shorted_rows)
            session.add(new_addition)
        session.commit()
    except Exception as e:
        print(e)


def check_username_exists(username):
    existing_user = session.query(
        UserNames).filter_by(username=username).first()
    return existing_user is not None


def check_for_late_messages():
    returning_list = []
    return returning_list


def check_new_prompt_exists(chat_id):
    existing_user = session.query(
        NewPrompt).filter_by(chat_id=chat_id).first()
    return existing_user is not None


def check_user_exists(chat_id: int):
    find_one = session.query(Users).filter_by(chat_id=chat_id).first()
    return True if find_one else False


def check_new_stage_exists():
    existing_user = session.query(
        AmoNewStages).first()
    return existing_user is not None


def check_shorted_history_exists(chat_id):
    existing_short_history = session.query(
        ShortedHistory).filter_by(chat_id=chat_id).first()
    return existing_short_history is not None


def check_name_exists(name):
    existing_user = session.query(UserNames).filter_by(name=name).first()
    return existing_user is not None


def add_new_username_and_name(chat_id):
    username = generate_random_string(12)
    while check_username_exists(username):
        username = generate_random_string(12)
    name = 'Клиент' + generate_random_digits(8)
    while check_name_exists(name):
        name = 'Клиент' + generate_random_digits(8)
    new_addition = UserNames(chat_id=chat_id, username=username, name=name)
    session.merge(new_addition)
    session.commit()


def add_new_amo_stage(chat_id, username, name, status_id):
    new_addition = AmoNewStages(
        chat_id=chat_id, username=username, name=name, status_id=status_id)
    session.merge(new_addition)
    session.commit()


def add_new_prompt(chat_id, prompt):
    new_addition = NewPrompt(chat_id=chat_id, prompt=prompt)
    session.merge(new_addition)
    session.commit()


def add_recent_message(chat_id, stage_in_amo):
    result = session.query(RecentMessages).filter_by(chat_id=chat_id).first()
    if result:
        if result.stage_in_amo not in ['142', '143']:
            new_addition = RecentMessages(
                chat_id=chat_id, time=datetime.now(), stage_in_amo=stage_in_amo)
            session.merge(new_addition)
            session.commit()
    else:
        new_addition = RecentMessages(
            chat_id=chat_id, time=datetime.now(), stage_in_amo=stage_in_amo)
        session.merge(new_addition)
        session.commit()


def add_new_lead_id(chat_id, lead_id):
    new_addition = LeadId(chat_id=chat_id, lead_id=lead_id)
    session.merge(new_addition)
    session.commit()


def add_in_users(user_name, name, chat_id, user_id):
    try:
        new_addition = Users(username=user_name, name=name,
                             chat_id=chat_id, user_id=user_id)
        session.merge(new_addition)
        session.commit()
        return True
    except:
        return False


def get_username_by_chat(chat_id: int):
    user = session.query(UserNames).filter_by(chat_id=chat_id).first()
    if user:
        return user.username
    else:
        return None


def get_lead_id_by_chat(chat_id: int):
    user = session.query(LeadId).filter_by(chat_id=chat_id).first()
    if user:
        return user.lead_id
    else:
        return None


def get_first_in_amo_stage():
    list_new = []
    user = session.query(AmoNewStages).first()
    if user:
        list_new.append(user.chat_id)
        list_new.append(user.username)
        list_new.append(user.name)
        list_new.append(user.status_id)
    else:
        pass
    return list_new


def get_chat_by_user_id(user_id):
    user = session.query(Users).filter_by(user_id=user_id).first()
    if user:
        return user.chat_id
    else:
        return None


def get_new_prompt(chat_id):
    user = session.query(NewPrompt).filter_by(chat_id=chat_id).first()
    if user:
        return user.prompt
    else:
        return None


def get_username_by_user_id(user_id):
    user = session.query(Users).filter_by(user_id=user_id).first()
    if user:
        return user.username
    else:
        return None


def get_name_by_user_id(user_id):
    user = session.query(Users).filter_by(user_id=user_id).first()
    if user:
        return user.name
    else:
        return None


def get_messages_from_client(chat_id: int):
    user = session.query(MessagesFromClient).filter_by(chat_id=chat_id).first()
    if user:
        return user.message_united
    else:
        return None


def get_shorted_history(chat_id):
    value = session.query(ShortedHistory).filter_by(chat_id=chat_id).all()
    returning_string = ''
    try:
        if value:
            for row in value:
                returning_string += row.history
    except Exception as e:
        print(e)
    finally:
        return returning_string


def get_shorted_rows_history(chat_id):
    value = session.query(ShortedHistory).filter_by(chat_id=chat_id).first()
    if value:
        return value.shorted_rows
    else:
        return 0


def get_name_by_chat(chat_id: int):
    user = session.query(UserNames).filter_by(chat_id=chat_id).first()
    if user:
        return user.name
    else:
        return None


def get_first_message():
    first_record = session.query(ListOfNewMessages).first()
    returning_value = []
    if first_record:
        chat_id = first_record.chat_id
        new_message = first_record.new_message
        username = first_record.username
        name = first_record.name
        media_download_link = first_record.media_download_link
        file_name = first_record.file_name
        array = [chat_id, new_message, username,
                 name, media_download_link, file_name]
        returning_value = array
    return returning_value


def delete_first_message():
    try:
        first_record = session.query(ListOfNewMessages).first()
        if first_record:
            session.delete(first_record)
            session.commit()
    except Exception as e:
        print(str(e))


def delete_new_prompt(chat_id):
    all_records = session.query(NewPrompt).filter_by(chat_id=chat_id).first()
    if all_records:
        session.delete(all_records)
        session.commit()
    else:
        print(f'no new prompt for user {chat_id}')


def delete_amo_new_stage():
    try:
        first_record = session.query(AmoNewStages).first()
        if first_record:
            session.delete(first_record)
            session.commit()
    except Exception as e:
        print(str(e))


def has_first_message():
    returning_value = False
    try:
        first_record = session.query(ListOfNewMessages).first()
        if first_record:
            returning_value = True
    except Exception as e:
        print(str(e))
    finally:
        return returning_value


def print_all_messages():
    all_records = session.query(ListOfNewMessages).all()
    if all_records:
        for item in all_records:
            print('new message:', item.new_message)


def delete_all_messages():
    all_records = session.query(ListOfNewMessages).all()
    if all_records:
        for item in all_records:
            session.delete(item)
            session.commit()


def delete_none_stage():
    try:
        first_record = session.query(AmoNewStages).all()
        if first_record:
            for item in first_record:
                if not item.username or item.username is None or item.username == 'None':
                    session.delete(item)
                    session.commit()
    except Exception as e:
        print(str(e))


def add_recent_message_another_time(chat_id, stage_in_amo, time_hours):
    result = session.query(RecentMessages).filter_by(chat_id=chat_id).first()
    if result:
        if result.stage_in_amo not in ['142', '143']:
            new_addition = RecentMessages(
                chat_id=chat_id, time=datetime.now()+timedelta(hours=time_hours), stage_in_amo=stage_in_amo)
            session.merge(new_addition)
            session.commit()


def add_active(chat: str):
    activity = BotActivity(chat_id=chat, is_bot_active=True)
    session.merge(activity)
    session.commit()


def add_disactive(chat: str):
    activity = BotActivity(chat_id=chat)
    session.merge(activity)
    session.commit()


def add_free_bot(chat: int):
    activity = IsBotFree(chat_id=chat, is_bot_free=True)
    session.merge(activity)
    session.commit()


def update_true(chat: str):
    activity = session.query(BotActivity).filter_by(chat_id=chat).first()
    if activity:
        activity.is_bot_active = True
        session.commit()
    else:
        print('no chat id in table for update_true function')


def update_time_recent_message(chat_id):
    activity = session.query(RecentMessages).filter_by(chat_id=chat_id).first()
    if activity:
        activity.time = datetime.now()
        session.commit()
    else:
        print('no chat id in table for update_true function')


def check_recent_messages(minutes: int):
    current_time = datetime.now()
    list_of_not_recent = []
    try:
        activity = session.query(RecentMessages).all()
        if activity:
            for item in activity:
                time_since_last_message = current_time - item.time
                if time_since_last_message >= timedelta(minutes=minutes):
                    list_of_not_recent.append(
                        (item.chat_id, item.stage_in_amo, item.time))
        else:
            print('no chat id in table for update_true function')
    except Exception as e:
        print(str(e))
    finally:
        return list_of_not_recent


def delete_all_recent_messages():
    try:
        session.query(RecentMessages).delete()
        session.commit()
    except Exception as e:
        print(str(e))


def free_all_bot():
    activity = session.query(IsBotFree).all()
    if activity:
        for item in activity:
            item.is_bot_free = True
        session.commit()
    else:
        print('no chat id in table for update_true function')


def set_busy_bot(chat: int):
    activity = session.query(IsBotFree).filter_by(chat_id=chat).first()
    try:
        activity.is_bot_free = False
        session.commit()
    except Exception as e:
        print('no chat id in table for set_busy_bot function')


def set_free_bot(chat: int):
    activity = session.query(IsBotFree).filter_by(chat_id=chat).first()
    try:
        activity.is_bot_free = True
        session.commit()
    except Exception as e:
        print('no chat id in table for set_free_bot function')


def delete_recent_message(chat_id):
    result = session.query(RecentMessages).filter_by(chat_id=chat_id).first()
    if result:
        session.delete(result)
        session.commit()


def update_false(chat: str):
    try:
        activity = session.query(BotActivity).filter_by(chat_id=chat).first()

        if activity:
            activity.is_bot_active = False
            session.commit()
        else:
            print('no chat id in table for update_false function')
    except Exception as e:
        print(e)


def check_existing(chat: str):
    find_one = session.query(BotActivity).filter_by(chat_id=chat).first()
    return True if find_one else False


def check_bot_state_existing(chat: int):
    find_one = session.query(IsBotFree).filter_by(chat_id=chat).first()
    return True if find_one else False


def is_bot_active(chat: str):
    find_one = session.query(BotActivity).filter_by(
        chat_id=chat, is_bot_active=True).first()
    return True if find_one else False


def is_bot_free(chat: int):
    find_one = session.query(IsBotFree).filter_by(
        chat_id=chat, is_bot_free=True).first()
    return True if find_one else False


session.close()

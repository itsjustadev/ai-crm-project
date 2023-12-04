# coding: utf8
from logging import error
from sqlalchemy import create_engine, inspect, MetaData, Table, Column, Integer, String, insert, text, select

# Create a database engine
engine = create_engine('sqlite:///psy_bot.db')

# Create a metadata object
metadata = MetaData()

def create_dynamic_table(table_name, metadata):
    return Table(
        table_name,
        metadata,
        Column('id', Integer, primary_key=True),
        Column('client_manager_gpt', String(25), default=''),
        Column('message', String, default='')
    )


def create_new_history_table(chat_id, engine, metadata):
    try:
        table_name = f'history_chat_{chat_id}'
        dynamic_table = create_dynamic_table(table_name, metadata)
        dynamic_table.create(engine)
    except Exception as e:
        print(e)


def check_history_table_exists(chat_id, engine):
    try:
        table_name = f'history_chat_{chat_id}'
        with engine.connect() as connection:
            result = connection.execute(text(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"))
            return result.fetchone()
    except Exception as e:
        print(str(e))
        
        
        
        



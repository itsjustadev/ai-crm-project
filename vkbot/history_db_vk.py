# coding: utf8
from logging import error
from sqlalchemy import create_engine, inspect, MetaData, Table, Column, Integer, String, insert, text, select
from sqlalchemy.orm import declarative_base

# Create a database engine
engine = create_engine('sqlite:///bot_vk.db')
Base = declarative_base()

# Create a metadata object
metadata = MetaData()

# Define a function to dynamically create tables

inspector = inspect(engine)


def create_dynamic_table(table_name):
    return Table(
        table_name,
        metadata,
        Column('id', Integer, primary_key=True),
        Column('client_manager_gpt', String(25), default=''),
        Column('message', String, default='')
    )


def create_new_history_table(chat_id):
    try:
        table_name = f'history_chat_{chat_id}'
        dynamic_table = create_dynamic_table(table_name)
        dynamic_table.create(engine)
    except Exception as e:
        print(e)


def check_history_table_exists(chat_id):
    table_name = f'history_chat_{chat_id}'
    return inspector.has_table(table_name)


def get_history(chat_id):
    dictation = []
    table_name = f'history_chat_{chat_id}'
    try:
        with engine.connect() as connection:
            result = connection.execute(text(f"SELECT * FROM {table_name}"))
            for row in result:
                role = row.client_manager_gpt
                if role == 'client':
                    dictation.append({'role': 'user', 'content': row.message})
                if role == 'manager' or role == 'gpt':
                    dictation.append(
                        {'role': 'assistant', 'content': row.message})
    except Exception as e:
        print(e)
    finally:
        return dictation
    
    
def get_not_shorted_history(chat_id, shorted_rows: int):
    dictation = []
    table_name = f'history_chat_{chat_id}'
    try:
        with engine.connect() as connection:
            result = connection.execute(text(f"SELECT * FROM {table_name} LIMIT -1 OFFSET {shorted_rows}"))
            for row in result:
                role = row.client_manager_gpt
                if role == 'client':
                    dictation.append({'role': 'user', 'content': row.message})
                if role == 'manager' or role == 'gpt':
                    dictation.append(
                        {'role': 'assistant', 'content': row.message})
    except Exception as e:
        print(e)
    finally:
        return dictation
    
    
def has_history_with_gpt(chat_id):
    returning_value = False
    table_name = f'history_chat_{chat_id}'
    try:
        with engine.connect() as connection:
            result = connection.execute(text(f"SELECT * FROM {table_name}"))
            for row in result:
                role = row.client_manager_gpt
                if role == 'gpt':
                    returning_value = True
    except Exception as e:
        print(e)
    finally:
        return returning_value
    
def get_last_id_history(chat_id):
    returning_value = False
    table_name = f'history_chat_{chat_id}'
    try:
        with engine.connect() as connection:
            result = connection.execute(text(f"SELECT id FROM {table_name} ORDER BY id DESC LIMIT 1"))
            for row in result:
                returning_value = row[0]
    except Exception as e:
        print(e)
    finally:
        return returning_value

def insert_history(chat_id, client_manager_gpt: str, message: str):
    table_name = f'history_chat_{chat_id}'
    try:
        with engine.connect() as connection:
            connection.execute(text(
                f'''INSERT INTO {table_name} (client_manager_gpt, message) VALUES ('{client_manager_gpt}', '{message}');'''))
            connection.commit()
    except Exception as e:
        print(e)
        
def delete_history(chat_id):
    table_name = f'history_chat_{chat_id}'
    try:
        with engine.connect() as connection:
            connection.execute(text(
                f'''DELETE FROM {table_name};'''))
            connection.commit()
    except Exception as e:
        print(e)
        

def replace_single_quotes_with_double(input_string):
    try:
        output_string = input_string.replace("'", "\"")
        return output_string
    except Exception as e:
        print(e)

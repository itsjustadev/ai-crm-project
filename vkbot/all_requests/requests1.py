from dotenv import load_dotenv
import os
import requests
import hashlib
import hmac
import json
from datetime import datetime
import pytz
import random
import string
import time
import logging


load_dotenv()
secret = str(os.getenv('SECRET'))
amojo_id = str(os.getenv('AMOJO_ID'))
method = 'POST'
content_type = 'application/json'
timezone = pytz.timezone('Europe/Moscow')
date = datetime.now().astimezone(timezone).strftime('%a, %d %b %Y %H:%M:%S %z')
path = '/v2/origin/custom/77cee4a3-57ff-48b0-aebb-ebb025491003_a79933f4-9e39-4438-bc0a-89ffc20b0b55/chats'
url = "https://amojo.amocrm.ru" + path
path1 = '/v2/origin/custom/77cee4a3-57ff-48b0-aebb-ebb025491003_a79933f4-9e39-4438-bc0a-89ffc20b0b55'
url1 = "https://amojo.amocrm.ru" + path1

# Создайте новый логгер
amo_in_logger = logging.getLogger('amo_in_logger')
amo_in_logger.setLevel(logging.INFO)
# Создайте обработчик и форматтер для логгера (пример)
file_handler = logging.FileHandler('logs/amo_in_message_log.log')
# Добавьте обработчик к логгеру
amo_in_logger.addHandler(file_handler)

amo_out_logger = logging.getLogger('amo_out_logger')
amo_out_logger.setLevel(logging.INFO)
# Создайте обработчик и форматтер для логгера (пример)
file_handler1 = logging.FileHandler('logs/amo_out_message_log.log')
# Добавьте обработчик к логгеру
amo_out_logger.addHandler(file_handler1)


def forming_body(chat_id, user_id, user_name):
    body = {
        "conversation_id": "skt-8e3e7640-49af-4448-a2c6-" + chat_id,
        "source": {
            "external_id": "leadgrambot"
        },
        "user": {
            "id": "skt-1376265f-86df-4c49-a0c3-" + user_id,
            "name": user_name,
            "profile": {
                "phone": "79151112290",
                "email": "example6.client@example.com"
            }
        }
    }
    return body


def forming_body1(chat_id, user_id, user_name, message_text):
    characters = list(string.digits + string.ascii_lowercase)
    random.shuffle(characters)
    random_sequence = ''.join(random.choices(characters, k=12))
    timestamp = int(time.time())
    msec_timestamp = int(time.time() * 1000)
    body1 = {
        "event_type": "new_message",
        "payload": {
            "timestamp": timestamp,
            "msec_timestamp": msec_timestamp,
            "msgid": "intt-" + random_sequence,
            "conversation_id": "skt-8e3e7640-49af-4448-a2c6-" + chat_id,
            "sender": {
                "id": "skt-1376265f-86df-4c49-a0c3-" + user_id,
                "profile": {
                    "phone": "+79151112990",
                    "email": "example6.client@example.com"
                },
                "name": user_name
            },
            "message": {
                "type": "text",
                "text": message_text
            },
            "silent": False
        }
    }
    return body1


def forming_body_for_files(chat_id, user_id, user_name, download_url):
    characters = list(string.digits + string.ascii_lowercase)
    random.shuffle(characters)
    random_sequence = ''.join(random.choices(characters, k=12))
    timestamp = int(time.time())
    msec_timestamp = int(time.time() * 1000)
    body1 = {
        "event_type": "new_message",
        "payload": {
            "timestamp": timestamp,
            "msec_timestamp": msec_timestamp,
            "msgid": "intt-" + random_sequence,
            "conversation_id": "skt-8e3e7640-49af-4448-a2c6-" + chat_id,
            "sender": {
                "id": "skt-1376265f-86df-4c49-a0c3-" + user_id,
                "profile": {
                    "phone": "+79151112990",
                    "email": "example6.client@example.com"
                },
                "name": user_name
            },
            "message": {
                "type": "file",
                "media": download_url
            },
            "silent": False
        }
    }
    return body1


def forming_body_for_pictures(chat_id, user_id, user_name, download_url):
    characters = list(string.digits + string.ascii_lowercase)
    random.shuffle(characters)
    random_sequence = ''.join(random.choices(characters, k=12))
    timestamp = int(time.time())
    msec_timestamp = int(time.time() * 1000)
    body1 = {
        "event_type": "new_message",
        "payload": {
            "timestamp": timestamp,
            "msec_timestamp": msec_timestamp,
            "msgid": "intt-" + random_sequence,
            "conversation_id": "skt-8e3e7640-49af-4448-a2c6-" + chat_id,
            "sender": {
                "id": "skt-1376265f-86df-4c49-a0c3-" + user_id,
                "profile": {
                    "phone": "+79151112990",
                    "email": "example6.client@example.com"
                },
                "name": user_name
            },
            "message": {
                "type": "picture",
                "media": download_url
            },
            "silent": False
        }
    }
    return body1


def forming_body_answer(chat_id, user_id, user_name, outgoing_message_text):
    characters = list(string.digits + string.ascii_lowercase)
    random.shuffle(characters)
    random_sequence = ''.join(random.choices(characters, k=12))
    timestamp = int(time.time())
    msec_timestamp = int(time.time() * 1000)
    body_answer = {
        "event_type": "new_message",
        "payload": {
            "timestamp": timestamp + 1,
            "msec_timestamp": msec_timestamp + 1000,
            "msgid": "intt-" + random_sequence,
            "conversation_id": "skt-8e3e7640-49af-4448-a2c6-" + chat_id,
            "sender": {
                "id": "skt-1376265f-86df-4c49-a0c3",
                "name": "Bot",
                "ref_id": "f1910c7f-b1e0-4184-bd09-c7def2a9109a"
            },
            "receiver": {
                "id": "skt-1376265f-86df-4c49-a0c3-" + user_id,
                "name": user_name,
                "profile": {
                    "phone": "+79151112990",
                    "email": "example6.client@example.com"
                }
            },
            "message": {
                "type": "text",
                        "text": outgoing_message_text
            },
            "silent": False
        }
    }
    return body_answer


def amo_chat_create(chat_id: str, user_id: str, user_name: str):
    body = forming_body(chat_id, user_id, user_name)

    request_body = json.dumps(body)
    check_sum = hashlib.md5(request_body.encode()).hexdigest()

    str_to_sign = "\n".join([
        method,
        check_sum,
        content_type,
        date,
        path,
    ])

    signature = hmac.new(secret.encode(), str_to_sign.encode(),
                         hashlib.sha1).hexdigest()

    headers = {
        'Date': date,
        'Content-Type': content_type,
        'Content-MD5': check_sum.lower(),
        'X-Signature': signature.lower(),
    }
    response = requests.post(url, data=request_body, headers=headers)

    print("Status:", response.status_code)
    print(response.text)
    return response


def amo_share_incoming_message(chat_id: str, user_id: str, user_name: str, message_text: str):
    body1 = forming_body1(chat_id, user_id, user_name, message_text)
    logging.basicConfig(filename='amo_logs.txt', level=logging.INFO)
    request_body = json.dumps(body1)
    check_sum = hashlib.md5(request_body.encode()).hexdigest()

    str_to_sign = "\n".join([
        method,
        check_sum,
        content_type,
        date,
        path1,
    ])

    signature = hmac.new(secret.encode(), str_to_sign.encode(),
                         hashlib.sha1).hexdigest()

    headers = {
        'Date': date,
        'Content-Type': content_type,
        'Content-MD5': check_sum.lower(),
        'X-Signature': signature.lower(),
    }
    response = requests.post(url1, data=request_body, headers=headers)
    print("Status:", response.status_code)
    print(response.text)
    # Получение текущего времени
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
    amo_in_logger.info("Время запроса: %s , Запрос: URL=%s, Тело=%s, Ответ=%s",
                       formatted_time, url, body1, response.text)
    return response.status_code


def amo_share_incoming_file(chat_id: str, user_id: str, user_name: str, download_url: str):
    body1 = forming_body_for_files(chat_id, user_id, user_name, download_url)

    request_body = json.dumps(body1)
    check_sum = hashlib.md5(request_body.encode()).hexdigest()

    str_to_sign = "\n".join([
        method,
        check_sum,
        content_type,
        date,
        path1,
    ])

    signature = hmac.new(secret.encode(), str_to_sign.encode(),
                         hashlib.sha1).hexdigest()

    headers = {
        'Date': date,
        'Content-Type': content_type,
        'Content-MD5': check_sum.lower(),
        'X-Signature': signature.lower(),
    }
    response = requests.post(url1, data=request_body, headers=headers)

    print("Status:", response.status_code)
    print(response.text)
    return response.status_code


def amo_share_incoming_picture(chat_id: str, user_id: str, user_name: str, download_url: str):
    body1 = forming_body_for_pictures(
        chat_id, user_id, user_name, download_url)

    request_body = json.dumps(body1)
    check_sum = hashlib.md5(request_body.encode()).hexdigest()

    str_to_sign = "\n".join([
        method,
        check_sum,
        content_type,
        date,
        path1,
    ])

    signature = hmac.new(secret.encode(), str_to_sign.encode(),
                         hashlib.sha1).hexdigest()

    headers = {
        'Date': date,
        'Content-Type': content_type,
        'Content-MD5': check_sum.lower(),
        'X-Signature': signature.lower(),
    }
    response = requests.post(url1, data=request_body, headers=headers)

    print("Status:", response.status_code)
    print(response.text)
    return response.status_code


def amo_share_outgoing_message(chat_id: str, user_id: str, user_name: str, message_text: str):
    body2 = forming_body_answer(chat_id, user_id, user_name, message_text)

    request_body = json.dumps(body2)
    check_sum = hashlib.md5(request_body.encode()).hexdigest()

    str_to_sign = "\n".join([
        method,
        check_sum,
        content_type,
        date,
        path1,
    ])

    signature = hmac.new(secret.encode(), str_to_sign.encode(),
                         hashlib.sha1).hexdigest()

    headers = {
        'Date': date,
        'Content-Type': content_type,
        'Content-MD5': check_sum.lower(),
        'X-Signature': signature.lower(),
    }
    response = requests.post(url1, data=request_body, headers=headers)

    print("Status:", response.status_code)
    print(response.text)
    # Получение текущего времени
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
    amo_in_logger.info("Время запроса: %s , Запрос: URL=%s, Тело=%s, Ответ=%s",
                       formatted_time, url, body2, response.text)

    return response.status_code

import json
from datetime import datetime
import logging
import requests
import pytz
from dotenv import load_dotenv
from all_requests.upload_file import upload_file
import os
import math
import time

load_dotenv()
timezone = pytz.timezone('Europe/Moscow')
date = datetime.now().astimezone(timezone).strftime('%a, %d %b %Y %H:%M:%S %z')
SECRET_FOR_ANALYSIS = str(os.getenv('SECRET_FOR_ANALYSIS'))
url_entity_base = "https://leadgramstudio.amocrm.ru" + '/api/v4/leads/'
url_user_id_base = "https://leadgramstudio.amocrm.ru" + \
    '/api/v4/contacts/chats?contact_id='
LOGS_PATH = str(os.getenv('LOGS_PATH'))
logging.basicConfig(filename=LOGS_PATH, level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - Line %(lineno)d')
# url_base =  "https://leadgramstudio.amocrm.ru" + '/api/v4/talks?id=5ae8014a-61ef-4d0a-a2a9-1995d8b59824'


def start_analysis_session(group_vk):
    group_vk = str(group_vk)
    url = f'http://vds2361288.my-ihor.ru/analyse'
    data = {"secret": SECRET_FOR_ANALYSIS,
            "group": group_vk
            }
    returning_value = None
    try:
        response = requests.post(url, json=data)
        returning_value = json.loads(response.text)
        returning_value = returning_value.get('key')
    except Exception as e:
        print('exception', str(e))
    finally:
        return returning_value


def get_analysis(group_vk, key):
    group_vk = str(group_vk)
    url = f'http://vds2361288.my-ihor.ru/analysis-result?secret={SECRET_FOR_ANALYSIS}&key={key}'
    returning_value = None
    try:
        response = requests.get(url)
        returning_value = json.loads(response.text)
        print(returning_value.get("status"))
        if returning_value.get("status") == "done":
            returning_value = returning_value.get("value")
        elif returning_value.get("status") == "pending":
            returning_value = "waiting"
        elif returning_value.get("status") == "error":
            returning_value = returning_value.get("error")
        else:
            returning_value = None
    except Exception as e:
        print('exception', str(e))
    finally:
        return returning_value

# key_for_analysis = start_analysis_session('tproger_web')
# analysis_text = None
# analysis_text = get_analysis('tproger_web', key_for_analysis)
# while analysis_text == 'waiting':
#     time.sleep(15)
#     analysis_text = get_analysis('tproger_web', key_for_analysis)
# print(analysis_text)
# if not analysis_text:
#     print('error')


def body_for_files(name_of_file: str, file_size: int):
    body = {
        "file_name": name_of_file,
        "file_size": file_size
    }
    return body


def body_for_token(refresh_token):
    body = {
        "client_id": "b0213b9e-fc9e-4831-98c9-0613e6851a6c",
        "client_secret": "ieFgifP1pzp0Wf1B4oCroX0ZkfVUDGkLx9NvXIF0DpG5kc7cUVNkBHQT7PsHFdkk",
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "redirect_uri": "http://itsonlychatgptbot.com/"
    }
    return body


def update_refresh_token(response):
    data = response.json()
    # Замените 'new_token_key' на ключ вашей переменной
    new_access_token = data['access_token']
    new_refresh_token = data['refresh_token']

    # Шаг 3: Обновите значение существующей переменной в файле среды
    load_dotenv('.env')  # Загружаем переменные из файла среды
    with open('.env', 'r') as env_file:
        lines = env_file.readlines()

    with open('.env', 'w') as env_file:
        for line in lines:
            key, value = line.strip().split('=')
            if key == 'REFRESH_TOKEN':  # Замените 'new_refresh_token' на имя вашей переменной
                line = f"{key}={new_refresh_token}\n"
            if key == 'ACCESS_TOKEN':  # Замените 'new_refresh_token' на имя вашей переменной
                line = f"{key}={new_access_token}\n"
            env_file.write(line)

    # Шаг 4: Используйте os.environ для немедленной установки нового значения переменной в текущем сеансе
    os.environ['REFRESH_TOKEN'] = new_refresh_token
    os.environ['ACCESS_TOKEN'] = new_access_token


def update_token():
    load_dotenv()
    refresh_token = str(os.getenv('REFRESH_TOKEN'))
    url = 'https://leadgramstudio.amocrm.ru' + '/oauth2/access_token'
    body = body_for_token(refresh_token)

    request_body = json.dumps(body)

    headers = {
        'Date': date,
        'Content-Type': 'application/json'
    }
    response = requests.post(url, data=request_body, headers=headers)

    if response.status_code == 200:
        update_refresh_token(response)
        print('token updated')
    else:
        print('error updating token')
        return 0


def get_session_response(url, request_body):
    access_token = str(os.getenv('ACCESS_TOKEN'))
    headers = {
        'Date': date,
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.post(url, data=request_body, headers=headers)
    return response


def amo_change_vk_link(lead_id, link):
    url = "https://leadgramstudio.amocrm.ru" + '/api/v4/leads/'
    url += str(lead_id)
    access_token = str(os.getenv('ACCESS_TOKEN'))
    headers = {
        'Date': date,
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    data = {
        "custom_fields_values": [{"field_id": 284833, "field_name": "Ссылка на группу", "values": [{"value": f"{link}"}]}]
    }
    response = requests.patch(url, json=data, headers=headers)
    return response.text


def amo_set_lead_source(lead_id):
    url = "https://leadgramstudio.amocrm.ru" + '/api/v4/leads/'
    url += str(lead_id)
    access_token = str(os.getenv('ACCESS_TOKEN'))
    headers = {
        'Date': date,
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    data = {
        "custom_fields_values": [{"field_id": 693933, "field_name": "Источник", "values": [{"value": "leadgrambot"}]}]
    }
    response = requests.patch(url, json=data, headers=headers)
    return response.text


def amo_pipeline_change(lead_id, PIPELINE_ID, STATUS_ID):
    url = "https://leadgramstudio.amocrm.ru" + '/api/v4/leads/'
    url += str(lead_id)
    access_token = str(os.getenv('ACCESS_TOKEN'))
    headers = {
        'Date': date,
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    data = {
        "status_id": STATUS_ID,
        "pipeline_id": PIPELINE_ID
    }
    response = requests.patch(url, json=data, headers=headers)
    print(response.text)
    return response.text


def amo_change_lead_status(lead_id, status_id):
    url = "https://leadgramstudio.amocrm.ru" + '/api/v4/leads/'
    url += str(lead_id)
    status_id = int(status_id)
    access_token = str(os.getenv('ACCESS_TOKEN'))
    headers = {
        'Date': date,
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    data = {
        "status_id": status_id
    }
    response = requests.patch(url, json=data, headers=headers)
    return response.text


def cut_vk_url_link(link):
    parts = link.split("vk.com/")
    text = ''
    if len(parts) > 1:
        text_after_vk = parts[1]
        text = text_after_vk
    return text


def amo_get_vk_link(lead_id):
    result = ''
    try:
        url = "https://leadgramstudio.amocrm.ru" + '/api/v4/leads/'
        url += str(lead_id)
        access_token = str(os.getenv('ACCESS_TOKEN'))
        headers = {
            'Date': date,
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        vk_link = data['custom_fields_values'][0]['values'][0]['value']
        result = cut_vk_url_link(vk_link)
    except Exception as e:
        print(str(e))
    return result


def get_entity_id(url, lead_id):
    url += f'{lead_id}/links'
    returning_value = ''
    try:
        access_token = str(os.getenv('ACCESS_TOKEN'))
        headers = {
            'Date': date,
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(url, headers=headers)
        print(response.text)
        data = json.loads(response.text)
        returning_value = data['_embedded']['links'][0]['to_entity_id']
    except Exception as e:
        logging.error(str(e))
        logging.info('cant get entity_id in access_token.py')
    finally:
        return returning_value


# get_entity_id(url_entity_base, 24824873)
get_entity_id(url_entity_base, 24976893)


def get_amo_user(url, lead_id):
    url += f'{lead_id}?with=contacts'
    returning_value = ''
    try:
        access_token = str(os.getenv('ACCESS_TOKEN'))
        headers = {
            'Date': date,
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        returning_value = data['_embedded']['contacts'][0]['id']
    except Exception as e:
        logging.error(str(e), exc_info=True)
        logging.info('cant get amo_users in access_token.py')
    finally:
        return returning_value


def get_user_email(contact_id):
    url = f'https://leadgramstudio.amocrm.ru/api/v4/contacts/' + \
        str(contact_id)
    returning_value = ''
    try:
        access_token = str(os.getenv('ACCESS_TOKEN'))
        headers = {
            'Date': date,
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        returning_value = data['custom_fields_values'][1]['values'][0]['value']
    except Exception as e:
        logging.error(str(e), exc_info=True)
        logging.info('cant get amo_users in access_token.py')
    finally:
        return returning_value


def get_lead_source(url, lead_id):
    url += f'{lead_id}'
    returning_value = ''
    try:
        access_token = str(os.getenv('ACCESS_TOKEN'))
        headers = {
            'Date': date,
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        returning_value = data['custom_fields_values'][1]['values'][0]['value']
    except Exception as e:
        logging.error(str(e))
        logging.info('cant get entity_id in access_token.py')
    finally:
        return returning_value


def get_amo_user_id(url, entity_id):
    url += str(entity_id)
    returning_value = ''
    try:
        access_token = str(os.getenv('ACCESS_TOKEN'))
        headers = {
            'Date': date,
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        print(data)
        returning_value = data['_embedded']['chats'][0]['chat_id']
    except Exception as e:
        print(str(e))
        logging.error(str(e), exc_info=True)
        logging.info('cant get amo_user_id in access_token.py')
    finally:
        return returning_value
    
print(get_amo_user_id(url_user_id_base, 30810099))


def open_session(name_of_file: str, file_size: int):
    load_dotenv()
    url_for_files = str(os.getenv('URL_FOR_FILES'))
    url = url_for_files + '/v1.0/sessions'
    body = body_for_files(name_of_file, file_size)

    request_body = json.dumps(body)

    response = get_session_response(url, request_body)

    if response.status_code != 200:
        update_token()
        response = get_session_response(url, request_body)

    return response.text


def get_array_for_upload_file(name_of_file, file_size):
    try:
        json_answer = open_session(name_of_file, file_size)
        json_data = json.loads(json_answer)
        upload_url = json_data.get('upload_url')
        max_part_size = json_data.get('max_part_size')
        max_part_size = math.floor(max_part_size / 1000) * 1000
        returning_array = [upload_url, max_part_size]
    except Exception as e:
        print(e)
        returning_array = []
    return returning_array


def upload_file_to_crm(name_of_file: str, file_path: str, file_size: int):
    array_for_file = get_array_for_upload_file(name_of_file, file_size)
    if array_for_file:
        url = array_for_file[0]
        max_part_size = array_for_file[1]
        try:
            answer = upload_file(url, file_path, max_part_size)
            return answer
        except Exception as e:
            print(e)
    else:
        print('can\'t upload file')

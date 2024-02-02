from aiogram.types import chat
import databases.history_db as Tables
import all_requests.requests1 as AMO_functions
from all_requests import download_file
from dotenv import load_dotenv
import os
from aiogram import types
import logging
import asyncio
import databases.databases as BotActivity
import requests
import json
import datetime
import httpx
from constants import *
import pathlib
import all_requests.access_token as AMO_connection
from all_functions import BOT, AMO, Database, handle_user_messages, logger_controling_deals, logger_for_stage_start, logger_for_stages


async def handle_photo(message: types.Message, bot):
    '''
    # обработчик для отправленных пользователем фотографий и картинок
    '''

    try:
        chat_id = message.chat.id
        Database.check_chat_existing(str(chat_id))
        user_name = message.from_user.username
        first_name = message.from_user.first_name
        if not user_name or not first_name:
            user_name = str(BotActivity.get_username_by_chat(chat_id))
            first_name = str(BotActivity.get_name_by_chat(chat_id))
        else:
            user_name = str(message.from_user.username)
            first_name = str(message.from_user.first_name)
        # Получаем информацию о фото
        # Выбираем последнее (самое крупное) изображение
        photo_info = message.photo[-1]
        file_id = photo_info.file_id
        file_size = photo_info.file_size
        file_name = f"photo_{file_id}.jpg"
        # file_name = file_name.split('-', 1)[0]
        # Получаем путь к папке "downloads" внутри проекта
        download_dir = pathlib.Path("downloads")
        # Создаем папку "downloads", если её еще нет
        download_dir.mkdir(exist_ok=True)
        # Скачиваем файл по его file_id и сохраняем его в папку "downloads"
        await bot.download_file_by_id(file_id, str(download_dir / file_name))
        answer_json = AMO_connection.upload_file_to_crm(
            file_name, f'downloads/{file_name}', file_size)
        if answer_json:
            data = json.loads(answer_json)
            link_to_download = data["_links"].get("download").get("href")
            text = ''
            if message.text:
                text = message.text
            if message.caption:
                text += ' ' + message.caption
            response = AMO_functions.amo_share_incoming_picture(
                str(chat_id), user_name, first_name, link_to_download)
            if response != 200:
                await asyncio.sleep(5)
                response = AMO_functions.amo_share_incoming_picture(
                    str(chat_id), user_name, first_name, link_to_download)
                if response != 200:
                    await bot.send_message(CHAT_FOR_LOGS, f'Could not share picture to amo for {user_name}')
        try:
            os.remove(f'downloads/{file_name}')
        except Exception as e:
            await message.answer(f"Ошибка при удалении файла '{file_name}': {str(e)}")
    except Exception as e:
        logging.error(str(e), exc_info=True)


async def voice_handler(message: types.Message, bot):
    '''
    # обработчик для отправленных пользователем голосовых сообщений
    '''

    try:
        chat_id = message.chat.id
        Database.check_chat_existing(str(chat_id))
        user_name = message.from_user.username
        first_name = message.from_user.first_name
        if not user_name or not first_name:
            user_name = str(BotActivity.get_username_by_chat(chat_id))
            first_name = str(BotActivity.get_name_by_chat(chat_id))
        else:
            user_name = str(message.from_user.username)
            first_name = str(message.from_user.first_name)
        if message.voice:
            voice_info = message.voice
            file_id = voice_info.file_id
            file_unique_id = voice_info.file_unique_id  # Уникальный идентификатор файла
            file_size = voice_info.file_size
            # Путь к папке для загрузки
            download_dir = pathlib.Path("downloads")
            download_dir.mkdir(exist_ok=True)
            # Формирование имени файла
            file_name = f"{file_unique_id}.ogg"
            # Скачивание голосового сообщения
            await bot.download_file_by_id(file_id, str(download_dir / file_name))
            # Обработка файла (например, загрузка в CRM)
            answer_json = AMO_connection.upload_file_to_crm(
                file_name, f'downloads/{file_name}', file_size)
            if answer_json:
                data = json.loads(answer_json)
                link_to_download = data["_links"].get("download").get("href")
                text = ''
                if message.text:
                    text = message.text
                if message.caption:
                    text += ' ' + message.caption
                response = AMO_functions.amo_share_incoming_voice_message(
                    str(chat_id), user_name, first_name, link_to_download)
                if response != 200:
                    await asyncio.sleep(5)
                    response = AMO_functions.amo_share_incoming_voice_message(
                        str(chat_id), user_name, first_name, link_to_download)
                    if response != 200:
                        await bot.send_message(CHAT_FOR_LOGS, f'Could not share file to amo for {user_name}')
            # Удаление файла после обработки
            try:
                os.remove(str(download_dir / file_name))
            except Exception as e:
                print(f"Ошибка при удалении файла '{file_name}': {str(e)}")
    except Exception as e:
        logging.error(str(e), exc_info=True)


async def upload_file(message: types.Message, bot):
    '''
    # обработчик для отправленных пользователем файлов
    '''
    try:
        chat_id = message.chat.id
        Database.check_chat_existing(str(chat_id))
        user_name = message.from_user.username
        first_name = message.from_user.first_name
        if not user_name or not first_name:
            user_name = str(BotActivity.get_username_by_chat(chat_id))
            first_name = str(BotActivity.get_name_by_chat(chat_id))
        else:
            user_name = str(message.from_user.username)
            first_name = str(message.from_user.first_name)
        # Проверяем, содержит ли сообщение файл
        if message.document:
            # Получаем информацию о файле
            file_info = message.document
            file_id = file_info.file_id
            file_name = file_info.file_name
            file_size = file_info.file_size
            # Получаем путь к папке "downloads" внутри проекта
            download_dir = pathlib.Path("downloads")
            # Создаем папку "downloads", если её еще нет
            download_dir.mkdir(exist_ok=True)
            # Скачиваем файл по его file_id и сохраняем его в папку "downloads"
            await bot.download_file_by_id(file_id, str(download_dir / file_name))
            answer_json = AMO_connection.upload_file_to_crm(
                file_name, f'downloads/{file_name}', file_size)
            if answer_json:
                data = json.loads(answer_json)
                link_to_download = data["_links"].get("download").get("href")
                text = ''
                if message.text:
                    text = message.text
                if message.caption:
                    text += ' ' + message.caption
                response = AMO_functions.amo_share_incoming_file(
                    str(chat_id), user_name, first_name, link_to_download)
                if response != 200:
                    await asyncio.sleep(5)
                    response = AMO_functions.amo_share_incoming_file(
                        str(chat_id), user_name, first_name, link_to_download)
                    if response != 200:
                        await bot.send_message(CHAT_FOR_LOGS, f'Could not share file to amo for {user_name}')
            try:
                os.remove(f'downloads/{file_name}')
            except Exception as e:
                print(f"Ошибка при удалении файла '{file_name}': {str(e)}")
    except Exception as e:
        logging.error(str(e), exc_info=True)


async def receiver_chat_gpt(message, bot):
    '''
    # обработчик любых текстовых сообщений
    '''

    flag_first_message = False
    chat_id = message.chat.id
    if not Tables.check_history_table_exists(chat_id):
        flag_first_message = True
        await BOT.start_command(message, bot)
        await AMO.share_first_messages_with_amo(message, bot)
    if not BotActivity.check_bot_state_existing(chat_id):
        BotActivity.add_free_bot(chat_id)
    user_name = message.from_user.username
    first_name = message.from_user.first_name
    if not user_name or not first_name:
        user_name = str(BotActivity.get_username_by_chat(chat_id))
        first_name = str(BotActivity.get_name_by_chat(chat_id))
    else:
        user_name = str(message.from_user.username)
        first_name = str(message.from_user.first_name)
    if not flag_first_message:
        await AMO.send_message_to_amo(chat_id, user_name, first_name, message, bot)
    if message.reply_to_message:
        new_message = f'"{message.reply_to_message.text}"-'
        BotActivity.add_message_from_client(chat_id, new_message)
    BotActivity.add_message_from_client(chat_id, message.text)
    if BotActivity.is_bot_free(chat_id):
        asyncio.create_task(handle_user_messages(message, bot))
    else:
        logger_controling_deals.info(
            f'Bot is not free for {chat_id} '+str(datetime.datetime.now()), exc_info=True)


async def chat_join_request_handler(chat_join_request: types.ChatJoinRequest, bot):
    '''
    # обработчик для принятия заявки в канал
    '''

    try:
        chat_id = chat_join_request.chat.id
        user_id = chat_join_request.from_user.id
        username = chat_join_request.from_user.username
        first_name = chat_join_request.from_user.first_name
        url = f"https://api.telegram.org/bot{TOKEN_FOR_BOT}/approveChatJoinRequest"
        payload = {
            'chat_id': chat_id,
            'user_id': user_id
        }
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            logger_controling_deals.info(
                f'chat_join_request approved for {chat_id} '+str(datetime.datetime.now()), exc_info=True)
        message = MessageForStart(text='/start', chat_id=user_id, username=username,
                                  first_name=first_name, reply_to_message=None)
        await receiver_chat_gpt(message, bot)
        return response.json()
    except Exception as e:
        logging.error(str(e), exc_info=True)

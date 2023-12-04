import vk_api
from vk_api import longpoll
from vk_api.longpoll import VkLongPoll, VkEventType
import asyncio
import os
from dotenv import load_dotenv
# from requests1 import amo_share_incoming_message
import logging


logging.basicConfig(filename='vkbot/vk_bot_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

load_dotenv()
def write_msg(user_id, text):
    try:
        vk.method('messages.send', {'user_id': user_id, 'message': text, 'random_id': 0})
    except vk_api.ApiError as e:
        logging.error(str(e))
    
# async def start_command(message: types.Message):
#     chat_id = message.chat.id
#     BotActivity.add_disactive(str(chat_id))
#     user_name = str(message.from_user.username)
#     first_name = str(message.from_user.first_name)
#     if not user_name or not first_name:
#         BotActivity.add_new_username_and_name(chat_id)
#         user_name = str(BotActivity.get_username_by_chat(chat_id))
#         first_name = str(BotActivity.get_name_by_chat(chat_id))
#     if not check_history_table_exists(chat_id):
#         create_new_history_table(chat_id)
#     try:
#         # добавить not !!!!!!!!!!!!!!!!!!!!
#         if not check_history_table_exists(chat_id):
#             create_new_history_table(chat_id)
#         # при создании чата amo_chat_create получаем conversation_id и чат id
#         response = amo_chat_create(str(chat_id), user_name, first_name)
#         if response.status_code != 200:
#             await asyncio.sleep(5)
#             response = amo_chat_create(
#                 str(chat_id), user_name, first_name)
#             if response.status_code != 200:
#                 await bot.send_message(CHAT_FOR_LOGS, f'Could not create chat in amo for {user_name}')
#         received_data = json.loads(response.text)
#         user_id = received_data.get('id')
#         BotActivity.add_in_users(user_name, first_name, chat_id, user_id)
#         response = amo_share_incoming_message(
#             str(chat_id), user_name, first_name, message.text)
#         if response != 200:
#             await asyncio.sleep(5)
#             response = amo_share_incoming_message(
#                 str(chat_id), user_name, first_name, message.text)
#             if response != 200:
#                 await bot.send_message(CHAT_FOR_LOGS, f'Could not send message to amo for {user_name}')
#     except Exception as e:
#         logging.error(str(e))
#         await bot.send_message(CHAT_FOR_LOGS, f'Could not complete the start command in telegram for {user_name}'+str(e))


# API-ключ созданный ранее
token = str(os.getenv('TOKEN_FOR_VK'))

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)

# Работа с сообщениями

async def echo_bot():
    try:
        longpoll = VkLongPoll(vk)
        for message in longpoll.listen():
            if message.type == VkEventType.MESSAGE_NEW:
                if message.text != '' and message.to_me:
                    write_msg(message.user_id, message.text)
    except vk_api.VkApiError as e:
        logging.error(str(e))
    except Exception as e:
        logging.error('unknown_error in echo_bot'+ str(e))
                
                
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(echo_bot())
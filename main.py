from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import openai
import logging
import asyncio
import databases as BotActivity
from constants import *
from helpers_functions import *
from server_routes import router
from fastapi import FastAPI
import uvicorn


openai.api_key = TOKEN_FOR_CHAT_GPT
bot = Bot(token=TOKEN_FOR_BOT5)
dp = Dispatcher(bot, storage=MemoryStorage())
app = FastAPI()
app.include_router(router)


BotActivity.free_all_bot()
BotActivity.delete_none_stage()


# запуск бота
async def run_bot():
    await dp.start_polling()


def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8080)


# группировка всех задач вместе
async def main():
    await skip_updates(bot)
    loop = asyncio.get_event_loop()
    bot_task = loop.create_task(run_bot())
    flask_task = loop.run_in_executor(None, run_server)
    messages_task = loop.create_task(checking_messages(bot))

    # регистрация обработчиков
    dp.register_chat_join_request_handler(
        lambda chat_join_request: chat_join_request_handler(chat_join_request, bot))
    dp.register_message_handler(
        lambda message: receiver_chat_gpt(message, bot))
    dp.register_message_handler(
        lambda message: upload_file(message, bot), content_types=types.ContentType.DOCUMENT)
    dp.register_message_handler(
        lambda message: voice_handler(message, bot), content_types=types.ContentType.VOICE)
    dp.register_message_handler(
        lambda message: handle_photo(message, bot), content_types=types.ContentType.PHOTO)
    try:
        await asyncio.gather(bot_task, flask_task, messages_task)
    except KeyboardInterrupt:
        logging.info('Stopping the application...')
        for task in asyncio.all_tasks():
            task.cancel()
        await asyncio.gather(*asyncio.all_tasks(), return_exceptions=True)
    finally:
        await asyncio.gather(*asyncio.all_tasks(), return_exceptions=True)
        loop.close()

# запуск приложения
if __name__ == "__main__":
    asyncio.run(main())

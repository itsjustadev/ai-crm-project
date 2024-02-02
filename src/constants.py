import datetime
import os
from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()
TOKEN_FOR_CHAT_GPT = str(os.getenv('TOKEN_FOR_CHAT_GPT'))
TOKEN_FOR_BOT = str(os.getenv('TOKEN_FOR_BOT'))
LOGS_PATH = str(os.getenv('LOGS_PATH'))
CHAT_FOR_LOGS = str(os.getenv('CHAT_FOR_LOGS'))
MODEL_GPT = 'gpt-4'
STAGE_IN_AMO_1 = ''
STAGE_IN_AMO_2 = ''
STAGE_IN_AMO_3 = ''
STAGE_IN_AMO_4 = ''
STAGE_FOR_SALE = ''
STAGE_FOR_MANAGER = ''
STAGE_FOR_CLOSED_DEALS = ''
STAGE_FOR_DONE_DEALS = ''
PIPELINE_ID = 0
STATUS_ID = 0
URL_ENTITY_BASE = ''
URL_USER_ID_BASE = ''
DOCUMENT_PATH = ''
current_datetime = datetime.datetime.now()
future_date = datetime.date.today() + datetime.timedelta(days=5)
month_names = {
    1: "января",
    2: "февраля",
    3: "марта",
    4: "апреля",
    5: "мая",
    6: "июня",
    7: "июля",
    8: "августа",
    9: "сентября",
    10: "октября",
    11: "ноября",
    12: "декабря"
}
day = future_date.day
month = future_date.month
date_for_sales_offer = f"{day} {month_names[month]}"


CONTENT = ''
TEXT_FOR_START = ''
CONTENT1 = ''
CONTENT2 = ''
CONTENT3 = ''
CONTENT4 = ''
PART_OF_ANALYSIS = ''
CONTENT_FOR_MANAGER = ''
CONTENT_FOR_SALE1 = ''
CONTENT_FOR_SALE2 = ''
MESSAGE_FOR_SECRET = ''
TEXT_FOR_SECRET = ''
TEXT_FOR_SECRET2 = ''
TEXT_AFTER_ANALYSIS1 = ''
TEXT_AFTER_ANALYSIS2 = ''
# amo_stages и prompts должны совпадать по количеству

AMO_STAGES = [STAGE_IN_AMO_1, STAGE_IN_AMO_2, STAGE_IN_AMO_3, STAGE_IN_AMO_4]
PROMPTS = [CONTENT1, CONTENT2, CONTENT3, CONTENT4]


class Message(BaseModel):
    id: str
    type: str
    text: str
    markup: str
    tag: str
    media: str
    thumbnail: str
    file_name: str
    file_size: int


class IncomingMessage(BaseModel):
    account_id: str
    time: int
    message: dict


class MessageForStart:
    def __init__(self, text, chat_id, username, first_name, reply_to_message):
        self.text = text
        self.chat = self.Chat(chat_id)
        self.from_user = self.User(username, first_name)
        self.reply_to_message = reply_to_message

    class Chat:
        def __init__(self, id):
            self.id = id

    class User:
        def __init__(self, username, first_name):
            self.username = username
            self.first_name = first_name

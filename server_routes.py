from fastapi import APIRouter, Request, HTTPException
from helpers_functions import function_for_initializing_conversation, helper_for_handle_amo_message, IncomingMessage, helper_for_redirect_leads, helper_for_handle_amo_stage_change

# !Раздел сервера!


router = APIRouter()


# эндпоинт срабатывающий при смене этапа для сделки в амо
@router.post("/json1222233jsdflfjblsa12")
async def handle_amo_stage_change(request: Request):
    await helper_for_handle_amo_stage_change(request, function_for_initializing_conversation)


# эндпоинт для перенаправления сделок с неразобранного в тестовую воронку
@router.post("/incomingleadsjson1222233jsdsdflf")
async def redirect_leads_to_pipeline(request: Request):
    await helper_for_redirect_leads(request)


# эндпоинт для сообщений отправленных из амо менеджером клиенту в бот
@router.post('/input_handler/{text}')
async def handle_amo_message(text: str, data: IncomingMessage, request: Request):
    await helper_for_handle_amo_message(text, data, request)

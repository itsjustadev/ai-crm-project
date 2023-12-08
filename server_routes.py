from fastapi import APIRouter, Request
from helpers_functions import function_for_initializing_conversation, helper_for_handle_amo_message, IncomingMessage, helper_for_psy_handle_amo_message, helper_for_redirect_leads

# !Раздел сервера!


router = APIRouter()


@router.post('/input_handler_psy_bot/{text}')
async def psy_handle_amo_message(text: str, data: IncomingMessage, request: Request):
    await helper_for_psy_handle_amo_message(data, request)

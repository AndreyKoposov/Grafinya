from fastapi.routing import APIRouter
from fastapi import Depends, Request

from src.app.db.engine import get_session
from src.app.services.assistant import Assistant
from src.app.schemas.messages import MessageData


router = APIRouter()

async def get_assistant(session=Depends(get_session, scope='function')) -> Assistant:
    return Assistant(session)

@router.get('/')
async def fetch(request: Request,
                assistant: Assistant = Depends(get_assistant)):
    user_id = request.cookies.get('grafinya_session')

    msgs = []
    if user_id:
        msgs = await assistant.fetch(user_id)

    return {
        'msgs': msgs
    }

@router.get('/check')
async def check(request: Request,
                assistant: Assistant = Depends(get_assistant)):
    user_id = request.cookies.get('grafinya_session')

    has_new = False
    ai_thinking = False
    if user_id:
        has_new = await assistant.has_unread(user_id)
        ai_thinking = await assistant.ai_thinking(user_id)

    return {
        'has_new': has_new,
        'ai_thinking': ai_thinking
    }

@router.post('/send')
async def send(request: Request,
               msg_data: MessageData,
               assistant: Assistant = Depends(get_assistant)):
    user_id = request.cookies.get('grafinya_session')

    to_wait = False
    if user_id:
        to_wait = await assistant.send(user_id, msg_data.text)

    return {
        'to_wait': to_wait
    }

from fastapi.routing import APIRouter
from fastapi import Depends, Request

from src.app.db.engine import get_session
from src.app.repositories.messages import MessageRepo
from src.app.services.assistant import Assistant
from src.app.schemas.messages import MessageData


router = APIRouter()

async def get_assistant(session=Depends(get_session, scope='function')) -> Assistant:
    msg_repo = MessageRepo(session)
    return Assistant(msg_repo)

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
    if user_id:
        has_new = await assistant.has_unread(user_id)

    return {
        'has_new': has_new
    }

@router.post('/send')
async def send(request: Request,
               msg_data: MessageData,
               assistant: Assistant = Depends(get_assistant)):
    user_id = request.cookies.get('grafinya_session')

    if user_id:
        await assistant.send(user_id, msg_data.text)

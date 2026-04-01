import re
from urllib.parse import unquote
from fastapi import APIRouter, Request, Response, Depends

from src.app.db.engine import get_session
from src.app.services.auth import AuthService


router = APIRouter()


async def get_auth_service(session=Depends(get_session, scope='function')) -> AuthService:
    return AuthService(session)

@router.post('/login')
async def login(request: Request,
                response: Response,
                auth: AuthService = Depends(get_auth_service)):

    orioks_identity = request.cookies.get('orioks_identity')
    if orioks_identity is None:
        return {
            'success': False,
            'error': 'Need orioks auth'
        }

    orioks_id = extract_orioks_id(orioks_identity)
    if not orioks_id:
        return {
            'success': False,
            'error': 'Cant parse orioks_id'
        }

    success, user_id = await auth.login_or_register(orioks_id)
    if success:
        response.set_cookie(key='grafinya_session', value=str(user_id))

    return {
        'success': success,
        'error': ""
    }


def extract_orioks_id(cookie_value):
    match = re.search(r'\[(\d+),', unquote(cookie_value))
    if match:
        return match.group(1)
    return None

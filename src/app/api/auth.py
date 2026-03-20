import re
from urllib.parse import unquote
from fastapi import APIRouter, Request, Response, Depends

from src.app.config import TEMPLATES
from src.app.db.engine import get_session
from src.app.repositories.user import UserRepo
from src.app.services.auth import AuthService


router = APIRouter()


async def get_auth_service(session=Depends(get_session)) -> AuthService:
    user_repo = UserRepo(session)
    return AuthService(user_repo)

@router.get('/')
def welcome(request: Request):
    context = {
        'request': request,
        'app_name': 'Grafinya',
        'app_header': 'Онтологический анализ процессов',
        'welcome_msg': 'Добро пожаловать! Представьтесь, пожалуйста',
    }
    return TEMPLATES.TemplateResponse('welcome.html', context=context)

@router.post('/login')
async def login(request: Request,
                response: Response,
                auth: AuthService = Depends(get_auth_service, scope='function')):

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

    success = await auth.login_or_register(orioks_id)
    if success:
        response.set_cookie(key='grafinya_session', value="true")

    return {
        'success': success,
        'error': ""
    }

@router.post('/logout')
def logout():
    pass

@router.get('/me')
def me():
    pass


def extract_orioks_id(cookie_value):
    match = re.search(r'\[(\d+),', unquote(cookie_value))
    if match:
        return match.group(1)
    return None

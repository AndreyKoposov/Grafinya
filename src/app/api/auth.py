from fastapi import APIRouter, Request, Response, Depends
from fastapi.templating import Jinja2Templates

from src.app.db.engine import get_session
from src.app.repositories.user import UserRepo
from src.app.services.auth import AuthService
from src.app.schemas.auth import LoginRequest


router = APIRouter()
templates = Jinja2Templates(directory='src/static/templates')

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
    return templates.TemplateResponse('welcome.html', context=context)

@router.post('/login')
async def login(#response: Response,
                request: LoginRequest,
                service: AuthService = Depends(get_auth_service)):

    print(request)
    result, is_new = await service.login_or_register(request)
    # response.set_cookie(key='test_cookie', value="test_value")

    return {
        'success': result.success,
        'error': result.error,
        'is_new': is_new
    }

@router.post('/logout')
def logout():
    pass

@router.get('/me')
def me():
    pass

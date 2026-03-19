from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory='src/static/templates')

@router.get('/')
def welcome(request: Request):
    context = {
        'request': request,
        'app_name': 'Grafinya',
        'app_header': 'Онтологический анализ процессов',
        'welcome_msg': 'Добро пожаловать! Представьтесь, пожалуйста'

    }
    return templates.TemplateResponse('welcome.html', context=context)

@router.post('/login')
def login():
    pass

@router.post('/logout')
def logout():
    pass

@router.get('/me')
def me():
    pass

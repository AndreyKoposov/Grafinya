from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from src.app.config import TEMPLATES
from src.app.api.router import router


app = FastAPI(title='Grafinya')
app.mount('/static', StaticFiles(directory='src/static'), name='static')

app.include_router(
    router,
    prefix='/api',
    tags=['api']
)

@app.get('/')
def home(request: Request):
    session = request.cookies.get('grafinya_session')

    if session is None:
        return TEMPLATES.TemplateResponse(request, 'welcome.html')

    return TEMPLATES.TemplateResponse(request, 'index.html')

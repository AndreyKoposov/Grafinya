from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from src.app.config import TEMPLATES, DEBUG
from src.app.api.router import router


app = FastAPI(title='Grafinya')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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

@app.head('/ping')
def ping():
    return Response(status_code=200)

if DEBUG:
    @app.get('/check_cookies')
    def check_cookies(request: Request):
        print("Received cookies:", dict(request.cookies))
        return Response(status_code=200)

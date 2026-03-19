from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.app.api.router import router


app = FastAPI(title='Grafinya')
app.mount('/static', StaticFiles(directory='src/static'), name='static')

app.include_router(
    router,
    prefix='/api',
    tags=['api']
)

@app.get('/')
def home():
    return RedirectResponse('/api/auth/')

@app.get('/dashboard')
def dashboard():
    return {'msg': 'Dashboard'}

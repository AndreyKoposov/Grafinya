from os.path import abspath
from os import getenv
from pathlib import Path
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates


ROOT = Path(abspath(__file__)).parent.parent.parent
TEMPLATES = Jinja2Templates(directory='src/static/templates')

load_dotenv(ROOT/'.env', encoding='utf-8')

DB_NAME = getenv('DB_NAME')
DB_USER = getenv('DB_USER')
DB_PSWRD = getenv('DB_PSWRD')
DB_HOST = getenv('DB_HOST')
DB_PORT = getenv('DB_PORT')

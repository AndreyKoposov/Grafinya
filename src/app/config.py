from os.path import abspath
from os import getenv
from pathlib import Path
from typing import Type, Optional
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates

from src.app.utils.any_parser import AnyParser, T


def get_env(key: str, to_type: Type[T] = str, default: Optional[T] = None) -> T:
    value = getenv(key)
    parsed = AnyParser.parse(value, to_type) if value else None

    if parsed is not None:
        return parsed
    if default is not None:
        return default

    raise ValueError("Error in parse .env")

ROOT = Path(abspath(__file__)).parent.parent.parent
TEMPLATES = Jinja2Templates(directory='src/static/templates')

load_dotenv(ROOT/'.env', encoding='utf-8')

AI_ENGINE = get_env('AI_ENGINE', default='GigaChat')
AI_MODEL = get_env('AI_MODEL')
AI_API_KEY = get_env('AI_API_KEY')
AI_TEMP = get_env('AI_TEMP', default=0.0, to_type=float)

DB_NAME = get_env('DB_NAME')
DB_USER = get_env('DB_USER')
DB_PSWRD = get_env('DB_PSWRD')
DB_HOST = get_env('DB_HOST')
DB_PORT = get_env('DB_PORT')

DEBUG = get_env('DEBUG', to_type=bool, default=False)

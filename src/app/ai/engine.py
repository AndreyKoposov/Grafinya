from abc import abstractmethod
import asyncio
import functools

from src.app.config import AI_ENGINE, AI_API_KEY, AI_MODEL, AI_TEMP
from src.app.ai.prompts import p_entities, p_stages, p_transitions, p_params
from src.app.utils.preprocessor import Preprocessor


class AIEngine():
    def __init__(self, max_pool: int = 10) -> None:
        self.semaphore = asyncio.Semaphore(max_pool)
        self.parser = Preprocessor()

    @abstractmethod
    async def chat(self, query: str) -> str:
        pass

    async def get_entities(self, text: str):
        raw_json = await self.chat(p_entities(text))
        return self.parser.preprocess(raw_json)['entities']

    async def get_stages(self, text: str):
        raw_json = await self.chat(p_stages(text))
        return self.parser.preprocess(raw_json)['stages']

    async def get_transitions(self, text: str, stages: list[str]):
        raw_json = await self.chat(p_transitions(text, stages))
        return self.parser.preprocess(raw_json)['transitions']

    async def get_params(self, text: str, stages: list[str]):
        raw_json = await self.chat(p_params(text, stages))
        return self.parser.preprocess(raw_json)['params']

    @staticmethod
    def with_semaphore(func):
        @functools.wraps(func)
        async def wrapper(self, *args, **kwargs):
            async with self.semaphore:
                result = await func(self, *args, **kwargs)
            return result
        return wrapper

    @staticmethod
    def get_engine() -> 'AIEngine':
        match AI_ENGINE:
            case 'GigaChat':
                from . import gigachat
                return gigachat.GigaChatEngine(AI_API_KEY, AI_MODEL, AI_TEMP)
            case _:
                raise ValueError("Unknown AI engine!")

engine = AIEngine.get_engine()

# Фотолитография — метод получения рисунка на поверхности материала. 
# На подложку наносится фоторезист, который засвечивается через фотошаблон, 
# проявляется, а затем используется для травления или напыления. 
# Фотолитография начинается с нанесения фоторезиста на подложку. 
# Затем происходит засвечивание через фотошаблон, проявление и 
# использование для травления или напыления.

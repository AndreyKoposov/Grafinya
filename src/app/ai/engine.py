from abc import abstractmethod

from src.app.config import AI_ENGINE, AI_API_KEY, AI_MODEL, AI_TEMP


class AIEngine():
    @abstractmethod
    async def chat(self, query: str) -> str:
        pass

def get_engine() -> AIEngine:
    match AI_ENGINE:
        case 'GigaChat':
            from . import gigachat
            return gigachat.GigaChatEngine(AI_API_KEY, AI_MODEL, AI_TEMP)
        case _:
            raise ValueError("Unknown AI engine!")

engine = get_engine()

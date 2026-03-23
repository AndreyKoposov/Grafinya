import json
from gigachat import GigaChat

from . import engine


class GigaChatEngine(engine.AIEngine):
    def __init__(self, key: str, model: str, temp: float) -> None:
        self.giga = GigaChat(
            credentials=key,
            model=model,
            verify_ssl_certs=False,
            temperature=temp,
            scope="GIGACHAT_API_PERS",
            timeout=30,
        )

    async def chat(self, query: str) -> str:
        response = await self.giga.achat(query)
        # print(json.loads(response.choices[0].message.content))
        return response.choices[0].message.content
# Привет, приведи список самых популярных языков программирования, только очень коротко, просто список и все
# Привет, это проверка, что API работает.
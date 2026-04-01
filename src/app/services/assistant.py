from uuid import UUID
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.db.engine import maker
from src.app.ai.engine import engine
from src.app.models.messages import Messages


class Assistant:
    def __init__(self, session: AsyncSession) -> None:
        self.s = session

    async def fetch(self, user_id: str) -> list:
        msgs = []
        for msg in await Messages.get_last_n(self.s, UUID(user_id), 30):
            msgs.append({
                'text': msg.text,
                'sender': msg.sender,
                'time': msg.created_at.strftime('%H:%M')
            })
            if isinstance(msg.id, UUID):
                await Messages.mark_read(self.s, msg.id)
        return msgs

    async def has_unread(self, user_id: str) -> bool:
        return await Messages.has_unread(self.s, UUID(user_id))

    async def send(self, user_id: str, text: str) -> bool:
        await Messages.create(self.s, UUID(user_id), text, 'user', True)

        if text.startswith('/'):
            await self.__do_command(user_id, text)
            return False

        asyncio.create_task(self.call_ai(user_id, text))
        return True

    async def __do_command(self, user_id: str, user_input: str):
        match user_input:
            case "/help":
                await self.__help(user_id)
            case "/ontology":
                await self.__ontology(user_id)
            case "/clear":
                await self.__clear(user_id)
            case _:
                await self.__unknown(user_id)

    async def __help(self, user_id: str):
        answer = "Список команд:\n"\
                 "\t/help - список команд\n"\
                 "\t/analyze - анализ описания процесса\n"\
                 "\t/ontology - отчет об онтологии процесса\n"\
                 "\t/clear - очистка чата\n"
        await self.__answer(user_id, answer)

    async def __ontology(self, user_id: str):
        answer = "На данный момент процесс состоит из 4 этапов"
        await self.__answer(user_id, answer)

    async def __clear(self, user_id: str):
        await Messages.delete_by_user(self.s, UUID(user_id))
        answer = "Чат очищен!"
        await self.__answer(user_id, answer)

    async def __unknown(self, user_id: str):
        answer = "Неизвестная команда, введите /help для просмотра списка доступных комманд."
        await self.__answer(user_id, answer)

    async def __answer(self, user_id: str, text: str):
        await Messages.create(self.s, UUID(user_id), text, 'ai', False)

    async def call_ai(self, user_id: str, text: str):
        async with maker() as session:
            try:
                response = await engine.chat(text)
                await Messages.create(session, UUID(user_id), response, 'ai', False)
                await session.commit()
            except Exception as e:
                await session.rollback()
                print(f"Ошибка сохранения ответа AI: {e}")
                raise

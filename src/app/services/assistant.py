from uuid import UUID
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.db.engine import maker
from src.app.ai.engine import engine
from src.app.models.messages import Messages
from src.app.models.user import User
from src.app.utils.state_manager import storage, State


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

    async def ai_thinking(self, user_id: str) -> bool:
        return await User.ai_thinking(self.s, UUID(user_id))

    async def send(self, user_id: str, text: str) -> bool:
        await Messages.create(self.s, UUID(user_id), text, 'user', True)

        if storage.get_state(user_id) == State.WAIT_TEXT:
            asyncio.create_task(self.start_analyze(user_id, text))
            storage.save_state(user_id, State.DEFAULT)
            return True

        if text.startswith('/'):
            await self.__do_command(user_id, text)
            return False

        asyncio.create_task(self.call_ai(user_id, text))
        return True

    async def __do_command(self, user_id: str, user_input: str):
        match user_input:
            case "/help":
                await self.__help(user_id)
            case "/analyze":
                await self.__analyze(user_id)
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

    async def __analyze(self, user_id: str):
        storage.save_state(user_id, State.WAIT_TEXT)
        answer = "Отправьте мне описание процесса, и я попробую разобраться!"
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

    async def start_analyze(self, user_id: str, user_input: str):
        async with maker() as session:
            try:
                await User.wait(session, UUID(user_id), True)
                await session.commit()
            except Exception as e:
                await session.rollback()
                print(f"Ошибка сохранения ответа AI: {e}")
                raise

        entities = await engine.get_entities(user_input)
        await self.call_ai(user_id, "Основные сущности процесса:\n- " + "\n- ".join(entities))

        stages = await engine.get_stages(user_input)
        await self.call_ai(user_id, "Основные этапы процесса:\n- " + "\n- ".join(stages))

        transitions = await engine.get_transitions(user_input, stages)
        await self.call_ai(user_id, "Основные переходы в процессе:\n- " + "\n- ".join(transitions))

        params = await engine.get_params(user_input, stages)
        await self.call_ai(user_id, self.__params_to_str(params))

        async with maker() as session:
            try:
                await User.wait(session, UUID(user_id), False)
                await session.commit()
            except Exception as e:
                await session.rollback()
                print(f"Ошибка сохранения ответа AI: {e}")
                raise

    def __params_to_str(self, stages_params: dict):
        """Преобразует JSON в текст для пользователя"""
        reply = ""

        for item in stages_params.items():
            reply += f"\n\nЭтап - {item[0]}"

            reply += "\nВыходные параметры:"
            for param in item[1]["main"]:
                name = param["name"]
                unit = param["unit"]
                value = param["output_value"]
                descr = param["description"]
                reply += f"\n\t- {name} | {unit} ({value}) | {descr}"

            reply += "\nУправляющие параметры:"
            for param in item[1]["control"]:
                name = param["name"]
                unit = param["unit"]
                value = param["input_value"]
                descr = param["description"]
                reply += f"\n\t- {name} | {unit} ({value}) | {descr}"

            reply += "\nВходные параметры:"
            for param in item[1]["input"]:
                name = param["name"]
                unit = param["unit"]
                value = param["input_value"]
                descr = param["description"]
                reply += f"\n\t- {name} | {unit} ({value}) | {descr}"

            reply += "\nОбеспечивающие параметры:"
            for param in item[1]["resource"]:
                name = param["name"]
                unit = param["unit"]
                value = param["expected_value"]
                result = param["result"]
                condition = param["condition"]
                descr = param["description"]
                reply += f"\n\t- {name} | {unit} ({condition} {value} => {result}) | {descr}"

        return reply
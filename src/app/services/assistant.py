from uuid import UUID

from src.app.repositories.messages import MessageRepo
from src.app.ai.engine import engine


class Assistant:
    def __init__(self, repo: MessageRepo) -> None:
        self.repo = repo

    async def fetch(self, user_id: str) -> list:
        msgs = []
        for msg in await self.repo.get_last_n(UUID(user_id), 30):
            msgs.append({
                'text': msg.text,
                'sender': msg.sender,
                'time': msg.created_at.strftime('%H:%M:%S')
            })
            if isinstance(msg.id, UUID):
                await self.repo.mark_read(msg.id)
        return msgs

    async def has_unread(self, user_id: str) -> bool:
        return await self.repo.has_unread(UUID(user_id))

    async def send(self, user_id: str, text: str):
        await self.repo.create(UUID(user_id), text, 'user', True)
        response = await engine.chat(text)
        await self.repo.create(UUID(user_id), response, 'ai', False)

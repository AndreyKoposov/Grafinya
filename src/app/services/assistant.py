from uuid import UUID

from src.app.repositories.messages import MessageRepo


class Assistant:
    def __init__(self, repo: MessageRepo) -> None:
        self.repo = repo

    async def has_unread(self, user_id: str) -> bool:
        return await self.repo.has_unread(UUID(user_id))

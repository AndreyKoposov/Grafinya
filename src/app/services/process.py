from uuid import UUID

from src.app.repositories.process import ProcessRepo


class ProcessService():
    def __init__(self, repo: ProcessRepo):
        self.repo = repo

    async def create(self, user_id: str, name: str) -> bool:
        await self.repo.create(UUID(user_id), name)
        return True

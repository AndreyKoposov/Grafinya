from uuid import UUID

from src.app.repositories.process import ProcessRepo


class ProcessService():
    def __init__(self, repo: ProcessRepo):
        self.repo = repo

    async def create(self, user_id: str, name: str) -> bool:
        await self.repo.create(UUID(user_id), name)
        return True

    async def get_all(self, user_id: str) -> list:
        pr_list = []
        for pr in await self.repo.get_by_user_id(UUID(user_id)):
            pr_list.append({
                'id': pr.id,
                'name': pr.name,
                'avatar': pr.name[0],
                'created': pr.created_at.strftime("%Y-%m-%d"),
                'option': 0,
                'count': 2
            })
        return pr_list

    async def rename(self, pr_id: str, new_name: str):
        await self.repo.rename(UUID(pr_id), new_name)

    async def delete(self, pr_id: str):
        await self.repo.delete(UUID(pr_id))

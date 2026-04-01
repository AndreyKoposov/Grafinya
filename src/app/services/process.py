from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.process import Process
from src.app.models.entities import Entity


class ProcessService():
    def __init__(self, session: AsyncSession):
        self.s = session

    async def create(self, user_id: str, name: str) -> bool:
        await Process.create(self.s, UUID(user_id), name)
        return True

    async def get_all(self, user_id: str) -> list:
        pr_list = []
        for pr in await Process.get_by_user_id(self.s, UUID(user_id)):
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
        await Process.rename(self.s, UUID(pr_id), new_name)

    async def delete(self, pr_id: str):
        await Process.delete(self.s, UUID(pr_id))

    async def update_entity(self, proc_id: str, e_id: str, name: str, tag: str):
        entity = await Entity.get_by_id(self.s, UUID(e_id))
        if entity:
            await Entity.update(self.s, UUID(e_id), name, tag)
        else:
            await Entity.create(self.s, UUID(proc_id), name, tag)

    async def delete_entity(self, e_id: str):
        await Entity.delete(self.s, UUID(e_id))

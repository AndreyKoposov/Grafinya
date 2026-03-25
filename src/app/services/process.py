from uuid import UUID

from src.app.repositories.process import ProcessRepo
from src.app.repositories.entities import EntityRepo
from src.app.repositories.parameters import ParamRepo


class ProcessService():
    def __init__(self, proc: ProcessRepo,
                 entity: EntityRepo,
                 param: ParamRepo):
        self.proc = proc
        self.entity = entity
        self.param = param

    async def create(self, user_id: str, name: str) -> bool:
        await self.proc.create(UUID(user_id), name)
        return True

    async def get_all(self, user_id: str) -> list:
        pr_list = []
        for pr in await self.proc.get_by_user_id(UUID(user_id)):
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
        await self.proc.rename(UUID(pr_id), new_name)

    async def delete(self, pr_id: str):
        await self.proc.delete(UUID(pr_id))

    async def update_entity(self, proc_id: str, e_id: str, name: str, tag: str):
        entity = await self.entity.get_by_id(UUID(e_id))
        if entity:
            await self.entity.update(UUID(e_id), name, tag)
        else:
            await self.entity.create(UUID(proc_id), name, tag)

    async def delete_entity(self, e_id: str):
        await self.entity.delete(UUID(e_id))

from typing import Optional
from uuid import UUID
from sqlalchemy import select, update, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.process import Entity


class EntityRepo():
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, entity_id: UUID) -> Optional[Entity]:
        query = select(Entity).where(Entity.id == entity_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_proc_id(self, proc_id: UUID) -> list[Entity]:
        query = select(Entity).where(Entity.proc_id == proc_id)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def create(self, proc_id: UUID, name: str, tag: str):
        query = insert(Entity).values(
            proc_id=proc_id,
            name=name,
            tag=tag
        )
        await self.session.execute(query)

    async def update(self, entity_id: UUID, name: str, tag: str):
        query = update(Entity).where(Entity.id==entity_id).values(name=name, tag=tag)
        await self.session.execute(query)

    async def delete(self, entity_id: UUID):
        query = delete(Entity).where(Entity.id==entity_id)
        await self.session.execute(query)

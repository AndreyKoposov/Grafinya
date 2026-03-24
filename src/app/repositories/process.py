from typing import Optional
from uuid import UUID
from sqlalchemy import select, update, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.process import Process


class ProcessRepo():
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, proc_id: UUID) -> Optional[Process]:
        query = select(Process).where(Process.id == proc_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: UUID) -> list[Process]:
        query = select(Process).where(Process.user_id == user_id)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def create(self, user_id: UUID, name: str):
        query = insert(Process).values(
            user_id=user_id,
            name=name
        )
        await self.session.execute(query)

    async def rename(self, proc_id: UUID, name: str):
        query = update(Process).where(Process.id==proc_id).values(name=name)
        await self.session.execute(query)

    async def delete(self, proc_id: UUID):
        query = delete(Process).where(Process.id==proc_id)
        await self.session.execute(query)

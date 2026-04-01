from typing import Optional
from uuid import uuid4
from uuid import UUID as ID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import select, update, insert, delete

from src.app.db.engine import base


class Entity(base):
    __tablename__ = 'entities'

    id = Column(UUID, primary_key=True, default=uuid4)
    proc_id = Column(UUID, ForeignKey('processes.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(50), nullable=False, index=True)
    tag = Column(Enum('human', 'machine', name='entity_tag'), nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Entity #{self.name}>"


    @staticmethod
    async def get_by_id(session: AsyncSession, entity_id: ID) -> Optional['Entity']:
        query = select(Entity).where(Entity.id == entity_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_proc_id(session: AsyncSession, proc_id: ID) -> list['Entity']:
        query = select(Entity).where(Entity.proc_id == proc_id)
        result = await session.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def create(session: AsyncSession, proc_id: ID, name: str, tag: str):
        query = insert(Entity).values(
            proc_id=proc_id,
            name=name,
            tag=tag
        )
        await session.execute(query)

    @staticmethod
    async def update(session: AsyncSession, entity_id: ID, name: str, tag: str):
        query = update(Entity).where(Entity.id==entity_id).values(name=name, tag=tag)
        await session.execute(query)

    @staticmethod
    async def delete(session: AsyncSession, entity_id: ID):
        query = delete(Entity).where(Entity.id==entity_id)
        await session.execute(query)

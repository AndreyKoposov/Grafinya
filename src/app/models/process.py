from uuid import uuid4
from uuid import UUID as ID
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy import select, insert, update, delete
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.db.engine import base


class Process(base):
    __tablename__ = 'processes'

    id = Column(UUID, primary_key=True, default=uuid4)
    user_id = Column(UUID, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(50), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Process #{self.name}>"


    @staticmethod
    async def get_by_id(session: AsyncSession, proc_id: ID) -> Optional['Process']:
        query = select(Process).where(Process.id == proc_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_user_id(session: AsyncSession, user_id: ID) -> list['Process']:
        query = select(Process).where(Process.user_id == user_id)
        result = await session.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def create(session: AsyncSession, user_id: ID, name: str):
        query = insert(Process).values(
            user_id=user_id,
            name=name
        )
        await session.execute(query)

    @staticmethod
    async def rename(session: AsyncSession, proc_id: ID, name: str):
        query = update(Process).where(Process.id==proc_id).values(name=name)
        await session.execute(query)

    @staticmethod
    async def delete(session: AsyncSession, proc_id: ID):
        query = delete(Process).where(Process.id==proc_id)
        await session.execute(query)

from uuid import uuid4
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, String, DateTime, select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import UUID

from src.app.db.engine import base


class User(base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, default=uuid4)
    orioks_id = Column(String(10), unique=True, nullable=True, index=True)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<User #{self.orioks_id}>"


    @staticmethod
    async def get_by_id(session: AsyncSession, user_id: UUID) -> Optional['User']:
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_orioks(session: AsyncSession, orioks_id: str) -> Optional['User']:
        query = select(User).where(User.orioks_id == orioks_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def create(session: AsyncSession, orioks_id: str):
        query = insert(User).values(
            orioks_id=orioks_id
        )
        await session.execute(query)

    @staticmethod
    async def update_last_login(session: AsyncSession, user_id: UUID):
        query = update(User).where(User.id == user_id).values(last_login=datetime.now())
        await session.execute(query)

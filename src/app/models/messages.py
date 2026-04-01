from uuid import uuid4
from uuid import UUID as ID
from datetime import datetime
from sqlalchemy import Column, Text, Enum, ForeignKey, DateTime, Boolean
from sqlalchemy import select, insert, update, delete, and_
from sqlalchemy.sql import functions
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import UUID

from src.app.db.engine import base


class Messages(base):
    __tablename__ = 'messages'

    id = Column(UUID, primary_key=True, default=uuid4)
    user_id = Column(UUID, ForeignKey('users.id', ondelete='CASCADE'))
    text = Column(Text, nullable=False)
    sender = Column(Enum('user', 'ai', name='sender'), nullable=False)
    read = Column(Boolean)
    created_at = Column(DateTime, default=datetime.now)


    def __repr__(self) -> str:
        return f"<Message {self.id}>"


    @staticmethod
    async def get_last_n(session: AsyncSession, user_id: ID, limit: int) -> list['Messages']:
        query = select(Messages)\
                .where(Messages.user_id == user_id)\
                .order_by(Messages.created_at)\
                .limit(limit)
        result = await session.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def has_unread(session: AsyncSession, user_id: ID) -> bool:
        query = select(functions.count()).select_from(Messages)\
            .where(and_(Messages.user_id == user_id, Messages.read == False))
        result = await session.execute(query)
        count = result.scalar()
        return count > 0 if count else False

    @staticmethod
    async def create(session: AsyncSession, user_id: ID, text: str, sender: str, read: bool):
        query = insert(Messages).values(
            user_id=user_id,
            text=text,
            sender=sender,
            read=read
        )
        await session.execute(query)

    @staticmethod
    async def mark_read(session: AsyncSession, msg_id: ID):
        query = update(Messages)\
                .where(Messages.id == msg_id)\
                .values(read=True)
        await session.execute(query)

    @staticmethod
    async def delete_by_user(session: AsyncSession, user_id: ID):
        query = delete(Messages).where(Messages.user_id == user_id)
        await session.execute(query)

from uuid import UUID
from sqlalchemy import select, insert, and_
from sqlalchemy.sql import functions
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.messages import Messages


class MessageRepo():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_last_n(self, user_id: UUID, limit: int) -> list[Messages]:
        query = select(Messages)\
                .where(Messages.user_id == user_id)\
                .order_by(Messages.created_at)\
                .limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def has_unread(self, user_id: UUID) -> bool:
        query = select(functions.count()).select_from(Messages)\
            .where(and_(Messages.user_id == user_id, Messages.read == False))
        result = await self.session.execute(query)
        count = result.scalar()
        return count > 0 if count else False

    async def create(self, user_id: UUID, text: str, sender: str, read: bool):
        query = insert(Messages).values(
            user_id=user_id,
            text=text,
            sender=sender,
            read=read
        )
        await self.session.execute(query)

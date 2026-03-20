from uuid import UUID
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, insert

from src.app.models.user import User


class UserRepo():
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_orioks(self, orioks_id: str) -> Optional[User]:
        query = select(User).where(User.orioks_id == orioks_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, orioks_id: str):
        query = insert(User).values(
            orioks_id=orioks_id
        )
        await self.session.execute(query)

    async def update_last_login(self, user_id: UUID):
        query = update(User).where(User.id == user_id).values(last_login=datetime.now(timezone.utc))
        await self.session.execute(query)

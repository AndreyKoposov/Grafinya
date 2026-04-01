from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.user import User


class AuthService():
    def __init__(self, session: AsyncSession):
        self.s = session

    async def login_or_register(self, orioks_id: str):
        existing_user = await User.get_by_orioks(self.s, orioks_id)
        if existing_user:
            return True, existing_user.id

        await User.create(self.s, orioks_id)
        new_user = await User.get_by_orioks(self.s, orioks_id)
        return True, new_user.id if new_user else None

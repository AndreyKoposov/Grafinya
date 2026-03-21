from uuid import UUID

from src.app.repositories.user import UserRepo


class AuthService():
    def __init__(self, repo: UserRepo):
        self.repo = repo

    async def login_or_register(self, orioks_id: str):
        existing_user = await self.repo.get_by_orioks(orioks_id)
        if existing_user:
            return True, existing_user.id

        await self.repo.create(orioks_id)
        new_user = await self.repo.get_by_orioks(orioks_id)
        return True, new_user.id if new_user else None

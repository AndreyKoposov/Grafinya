from src.app.repositories.user import UserRepo


class AuthService():
    def __init__(self, repo: UserRepo):
        self.repo = repo

    async def login_or_register(self, orioks_id: str) -> bool:
        existing_user = await self.repo.get_by_orioks(orioks_id)
        if existing_user:
            return True

        await self.repo.create(orioks_id)
        return True

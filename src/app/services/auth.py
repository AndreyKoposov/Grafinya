from src.app.repositories.user import UserRepo
from src.app.schemas.auth import LoginRequest, LoginResponse


class AuthService():
    def __init__(self, repo: UserRepo) -> None:
        self.repo = repo

    async def login_or_register(self, user_data: LoginRequest) -> tuple[LoginResponse, bool]:
        existing_user = await self.repo.get_by_name(user_data.name)

        if existing_user:
            return (LoginResponse(success=True, error=""), False)

        return await self.repo.create(user_data), True

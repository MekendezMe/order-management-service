from core.repositories.user_repository import UserRepository


class UserService:
    def __init__(self):
        self.user_repository = UserRepository(session: AsyncSession)
    async def register(self):

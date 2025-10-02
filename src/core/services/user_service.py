from core.constants import ROLE_USER
from core.exceptions.role import RoleNotFoundException
from core.exceptions.user import InvalidPasswordLengthException, UserAlreadyExistException, UserNotFoundException, \
    IncorrectPasswordException
from core.models import User
from core.repositories.role_repository import RoleRepository
from core.repositories.user_repository import UserRepository
from core.schemas.user import UserCreate, UserRead, UserLogin
from core.services.mappers.user_mapper import create_to_model, model_to_read


class UserService:
    def __init__(self, user_repository: UserRepository, role_repository: RoleRepository):
        self.user_repository = user_repository
        self.role_repository = role_repository

    async def register(self, user_create: UserCreate) -> UserRead:
        existing_user = await self.user_repository.get_by_email(user_create.email)
        if existing_user:
            raise UserAlreadyExistException()

        if len(user_create.password) < 8:
            raise InvalidPasswordLengthException()

        role = await self.role_repository.get_by_name(ROLE_USER)

        if role is None:
            raise RoleNotFoundException()

        user_model = create_to_model(user_create, role=role)

        new_user = await self.user_repository.create(user_model)

        return model_to_read(new_user)

    async def login(self, user_login: UserLogin) -> UserRead:
        existing_user = await self.user_repository.get_by_email(user_login.email)
        if existing_user is None:
            raise UserNotFoundException()

        if existing_user.password != user_login.password:
            raise IncorrectPasswordException()

        return model_to_read(existing_user)



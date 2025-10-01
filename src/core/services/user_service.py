from core.exceptions.role import RoleNotFoundException
from core.exceptions.user import InvalidPasswordLengthException, UserAlreadyExistException, UserNotFoundException, \
    IncorrectPasswordException
from core.models import User
from core.repositories.role_repository import RoleRepository
from core.repositories.user_repository import UserRepository
from core.schemas.user import UserCreate, UserRead, UserLogin


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

        role = await self.role_repository.get_by_name("user")

        if role is None:
            raise RoleNotFoundException()

        user_model = User(
            email=user_create.email,
            password=user_create.password,
            name=user_create.name,
            surname=user_create.surname,
            age=user_create.age,
            role_id=role.id,
        )

        new_user = await self.user_repository.create(user_model)

        return UserRead.model_validate(new_user)

    async def login(self, user_login: UserLogin) -> UserRead:
        existing_user = await self.user_repository.get_by_email(user_login.email)
        if existing_user is None:
            raise UserNotFoundException()

        if existing_user.password != user_login.password:
            raise IncorrectPasswordException()

        return UserRead.model_validate(existing_user)



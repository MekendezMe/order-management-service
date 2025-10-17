from datetime import timedelta

from core import constants
from core.config import settings
from core.constants import ROLE_USER
from core.exceptions.role import RoleNotFoundException
from core.exceptions.user import InvalidPasswordLengthException, UserAlreadyExistException, UserNotFoundException, \
    IncorrectPasswordException
from core.repositories.role_repository import RoleRepository
from core.repositories.user_repository import UserRepository
from core.schemas.user import UserCreate, UserRead, UserLogin, LoginResponse
from core.security.tokens_checker import create_access_token
from core.services.mappers.user_mapper import create_to_model, model_to_read
from utils.password_encryptor import hash_password, verify_password
from core.services.mappers import role_mapper


class UserService:
    def __init__(self, user_repository: UserRepository, role_repository: RoleRepository):
        self.user_repository = user_repository
        self.role_repository = role_repository


    async def register(self, user_create: UserCreate) -> UserRead:
        user = await self.user_repository.get_by_email(user_create.email)
        if user:
            raise UserAlreadyExistException()

        if len(user_create.password) < 8:
            raise InvalidPasswordLengthException()

        role = await self.role_repository.get_by_name(ROLE_USER)

        if role is None:
            raise RoleNotFoundException()

        converted_role = role_mapper.model_to_read(role)

        hashed_password = hash_password(user_create.password)

        user_model = create_to_model(user_create, hashed_password, role)

        new_user = await self.user_repository.create(user_model)

        return model_to_read(new_user, converted_role)

    async def login(self, user_login: UserLogin) -> LoginResponse:
        user = await self.user_repository.get_by_email(user_login.email)
        if not user:
            raise UserNotFoundException()

        if not verify_password(user_login.password, user.password):
            raise IncorrectPasswordException()

        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=timedelta(minutes=settings.jwt.access_token_expire_minutes)
        )

        converted_role = role_mapper.model_to_read(user.role)

        return LoginResponse(access_token=access_token, token_type=constants.TOKEN_TYPE, user=model_to_read(user, converted_role))

    async def confirm_email(self, email) -> bool:
        user = await self.user_repository.get_by_email(email)
        if not user:
            raise UserNotFoundException()

        user.confirmed = True

        updated_user = await self.user_repository.update(user)
        return updated_user.confirmed


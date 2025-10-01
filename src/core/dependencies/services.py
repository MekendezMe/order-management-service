from fastapi import Depends

from core.dependencies.repositories import get_user_repository, get_role_repository
from core.repositories.role_repository import RoleRepository
from core.repositories.user_repository import UserRepository
from core.services.user_service import UserService


async def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository),
        role_repository: RoleRepository = Depends(get_role_repository)
) -> UserService:
    return UserService(user_repository, role_repository)
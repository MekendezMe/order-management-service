from fastapi import Depends

from core.dependencies.repositories import get_user_repository, get_role_repository, get_product_repository, \
    get_author_repository
from core.repositories.role_repository import RoleRepository
from core.repositories.user_repository import UserRepository
from core.services.product_service import ProductService
from core.services.user_service import UserService

async def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository),
        role_repository: RoleRepository = Depends(get_role_repository)
) -> UserService:
    return UserService(user_repository, role_repository)

async def get_product_service(
        product_repository: UserRepository = Depends(get_product_repository),
        author_repository: RoleRepository = Depends(get_author_repository)
) -> ProductService:
    return ProductService(product_repository, author_repository)
from fastapi import Depends

from core.dependencies.repositories import get_user_repository, get_role_repository, get_product_repository, \
    get_author_repository, get_basket_repository
from core.repositories.author_repository import AuthorRepository
from core.repositories.basket_repository import BasketRepository
from core.repositories.product_repository import ProductRepository
from core.repositories.role_repository import RoleRepository
from core.repositories.user_repository import UserRepository
from core.services.basket_service import BasketService
from core.services.product_service import ProductService
from core.services.user_service import UserService

async def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository),
        role_repository: RoleRepository = Depends(get_role_repository)
) -> UserService:
    return UserService(user_repository, role_repository)

async def get_product_service(
        product_repository: ProductRepository = Depends(get_product_repository),
        author_repository: AuthorRepository = Depends(get_author_repository)
) -> ProductService:
    return ProductService(product_repository, author_repository)

async def get_basket_service(
        basket_repository: BasketRepository = Depends(get_basket_repository)
) -> BasketService:
    return BasketService(basket_repository)
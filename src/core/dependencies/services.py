from fastapi import Depends

from core.dependencies.repositories import get_user_repository, get_role_repository, get_product_repository, \
    get_author_repository, get_basket_repository, get_basket_product_repository
from core.repositories.author_repository import AuthorRepository
from core.repositories.basket_product_repository import BasketProductRepository
from core.repositories.product_repository import ProductRepository
from core.repositories.role_repository import RoleRepository
from core.repositories.user_repository import UserRepository
from core.services.basket_product_service import BasketProductService
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
        basket_product_repository: BasketProductRepository = Depends(get_basket_product_repository)
) -> BasketProductService:
    return BasketProductService(basket_product_repository)
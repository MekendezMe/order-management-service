from fastapi import Depends

from core.dependencies.repositories import get_user_repository, get_role_repository, get_product_repository, \
    get_author_repository, get_basket_repository, get_order_repository, get_order_status_repository, \
    get_order_product_repository
from core.repositories.author_repository import AuthorRepository
from core.repositories.basket_repository import BasketRepository
from core.repositories.order_product_repository import OrderProductRepository
from core.repositories.order_repository import OrderRepository
from core.repositories.product_repository import ProductRepository
from core.repositories.role_repository import RoleRepository
from core.repositories.status_repository import StatusRepository
from core.repositories.user_repository import UserRepository
from core.services.basket_service import BasketService
from core.services.order_service import OrderService
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
        basket_repository: BasketRepository = Depends(get_basket_repository),
        user_repository: UserRepository = Depends(get_user_repository),
        product_repository: ProductRepository = Depends(get_product_repository),
) -> BasketService:
    return BasketService(basket_repository, user_repository, product_repository)

async def get_order_service(
        basket_repository: BasketRepository = Depends(get_basket_repository),
        user_repository: UserRepository = Depends(get_user_repository),
        order_repository: OrderRepository = Depends(get_order_repository),
        product_repository: ProductRepository = Depends(get_product_repository),
        status_repository: StatusRepository = Depends(get_order_status_repository),
        order_product_repository: OrderProductRepository = Depends(get_order_product_repository)
) -> OrderService:
    return OrderService(basket_repository, user_repository, order_repository, product_repository, status_repository, order_product_repository)
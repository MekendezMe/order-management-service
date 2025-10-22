from typing import Annotated, Any, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.db_helper import db_helper
from core.repositories.author_repository import AuthorRepository
from core.repositories.basket_repository import BasketRepository
from core.repositories.order_product_repository import OrderProductRepository
from core.repositories.order_repository import OrderRepository
from core.repositories.product_repository import ProductRepository
from core.repositories.role_repository import RoleRepository
from core.repositories.status_repository import StatusRepository
from core.repositories.user_repository import UserRepository

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with db_helper.session_factory() as session:
        yield session


async def get_user_repository(
        session: AsyncSession = Depends(get_async_session)
) -> UserRepository:
    return UserRepository(session)

async def get_role_repository(
        session: AsyncSession = Depends(get_async_session)
) -> RoleRepository:
    return RoleRepository(session)

async def get_product_repository(
        session: AsyncSession = Depends(get_async_session)
) -> ProductRepository:
    return ProductRepository(session)

async def get_author_repository(
        session: AsyncSession = Depends(get_async_session)
) -> AuthorRepository:
    return AuthorRepository(session)

async def get_basket_repository(
        session: AsyncSession = Depends(get_async_session)
) -> BasketRepository:
    return BasketRepository(session)


async def get_order_repository(
        session: AsyncSession = Depends(get_async_session)
) -> OrderRepository:
    return OrderRepository(session)

async def get_order_status_repository(
        session: AsyncSession = Depends(get_async_session)
) -> StatusRepository:
    return StatusRepository(session)

async def get_order_product_repository(
        session: AsyncSession = Depends(get_async_session)
) -> OrderProductRepository:
    return OrderProductRepository(session)
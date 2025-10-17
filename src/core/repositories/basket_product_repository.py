from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import BasketProduct
from sqlalchemy import select

class BasketProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: int) -> BasketProduct | None:
        result = await self.session.execute(select(BasketProduct).options(selectinload(BasketProduct.user)).where(BasketProduct.id == id))
        basket = result.scalar_one_or_none()
        return basket

    async def get_by_user(self, user_id: int) -> BasketProduct | None:
        result = await self.session.execute(select(BasketProduct).options(selectinload(BasketProduct.user)).where(BasketProduct.user_id == user_id))
        basket = result.scalar_one_or_none()
        return basket

    async def get_all(self) -> list[BasketProduct]:
        result = await self.session.scalars(select(BasketProduct))
        baskets = result.all()
        return baskets

    async def create(self, user: User) -> User:
        try:
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except Exception as e:
            await self.session.rollback()
            print(f"Error creating user: {e}")
            raise


    async def update(self, user: User) -> User:
        try:
            user = await self.session.merge(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except Exception as e:
            await self.session.rollback()
            print(f"Error updating user: {e}")
            raise

    async def delete(self, id: int) -> bool:
        try:
            user = await self.session.get(User, id)
            await self.session.delete(user)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            print(f"Error updating user: {e}")
            raise
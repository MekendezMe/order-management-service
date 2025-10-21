from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from core.models import BasketProduct, User, Product
from sqlalchemy import select, delete

class BasketRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: int) -> BasketProduct | None:
        result = await self.session.execute(select(BasketProduct).
                                            options(joinedload(BasketProduct.user).joinedload(User.role)).
                                            options(joinedload(BasketProduct.product).joinedload(Product.author)).
                                            where(BasketProduct.id == id))
        basket = result.scalar_one_or_none()
        return basket

    async def get_by_user(self, user_id: int) -> BasketProduct | None:
        result = await self.session.execute(select(BasketProduct).
                                            options(joinedload(BasketProduct.user).joinedload(User.role)).
                                            options(joinedload(BasketProduct.product).joinedload(Product.author)).
                                            where(BasketProduct.user_id == user_id))
        basket = result.scalar_one_or_none()
        return basket

    async def get_user_items(self, user_id: int) -> list[BasketProduct]:
        result = await self.session.execute(select(BasketProduct).
                                            options(joinedload(BasketProduct.user).joinedload(User.role)).
                                            options(joinedload(BasketProduct.product).joinedload(Product.author)).
                                            where(BasketProduct.user_id == user_id))
        items = result.scalars().all()
        return items

    async def get_by_user_and_product(self, user_id: int, product_id: int) -> BasketProduct | None:
        result = await self.session.execute(select(BasketProduct).
                                            options(joinedload(BasketProduct.user).joinedload(User.role)).
                                            options(joinedload(BasketProduct.product).joinedload(Product.author)).
                                            where(BasketProduct.user_id == user_id,
                                                  BasketProduct.product_id == product_id))
        item = result.scalar_one_or_none()
        return item


    async def get_all(self) -> list[BasketProduct]:
        result = await self.session.scalars(select(BasketProduct).
                                            options(joinedload(BasketProduct.user).joinedload(User.role)).
                                            options(joinedload(BasketProduct.product).joinedload(Product.author)))
        baskets = result.all()
        return baskets

    async def create(self, basket: BasketProduct) -> BasketProduct:
        try:
            self.session.add(basket)
            await self.session.commit()
            await self.session.refresh(basket)
            return basket
        except Exception as e:
            await self.session.rollback()
            print(f"Error creating basket: {e}")
            raise


    async def update(self, basket: BasketProduct) -> BasketProduct:
        try:
            basket = await self.session.merge(basket)
            await self.session.commit()
            await self.session.refresh(basket)
            return basket
        except Exception as e:
            await self.session.rollback()
            print(f"Error updating basket: {e}")
            raise

    async def delete(self, id: int) -> bool:
        try:
            basket = await self.session.get(BasketProduct, id)
            await self.session.delete(basket)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            print(f"Error deleting basket: {e}")
            raise

    async def clear_user_basket(self, user_id: int) -> bool:
        try:
            statement = delete(BasketProduct).where(BasketProduct.user_id == user_id)
            await self.session.execute(statement)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            print("Error deleting user items:", e)
            raise

    async def clear_item_in_user_basket(self, user_id: int, product_id: int) -> bool:
        try:
            statement = delete(BasketProduct).where(BasketProduct.user_id == user_id,
                                                    BasketProduct.product_id == product_id)
            await self.session.execute(statement)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            print("Error deleting item from basket:", e)
            raise
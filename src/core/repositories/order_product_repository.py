from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.models import OrderProduct, Order, User, Product


class OrderProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: int) -> OrderProduct | None:
        result = await self.session.execute(select(OrderProduct).
                                            options(joinedload(OrderProduct.order).joinedload(Order.user).joinedload(User.role)).
                                            options(joinedload(OrderProduct.order).joinedload(Order.status)).
                                            options(joinedload(OrderProduct.product).joinedload(Product.author)).
                                            where(OrderProduct.id == id))
        order_product = result.scalar_one_or_none()
        return order_product

    async def get_by_order(self, order_id: int) -> OrderProduct | None:
        result = await self.session.execute(select(OrderProduct).
                                            options(
            joinedload(OrderProduct.order).joinedload(Order.user).joinedload(User.role)).
                                            options(joinedload(OrderProduct.order).joinedload(Order.status)).
                                            options(joinedload(OrderProduct.product).joinedload(Product.author)).
                                            where(OrderProduct.order_id == order_id))
        order_product = result.scalar_one_or_none()
        return order_product

    async def get_order_products(self, order_id: int) -> list[OrderProduct]:
        result = await self.session.execute(select(OrderProduct).
                                            options(
            joinedload(OrderProduct.order).joinedload(Order.user).joinedload(User.role)).
                                            options(joinedload(OrderProduct.order).joinedload(Order.status)).
                                            options(joinedload(OrderProduct.product).joinedload(Product.author)).
                                            where(OrderProduct.order_id == order_id))
        order_products = result.scalars().all()
        return order_products

    async def get_all(self) -> list[OrderProduct]:
        result = await self.session.execute(select(OrderProduct).
                                            options(
            joinedload(OrderProduct.order).joinedload(Order.user).joinedload(User.role)).
                                            options(joinedload(OrderProduct.order).joinedload(Order.status)).
                                            options(joinedload(OrderProduct.product).joinedload(Product.author)))
        order_products = result.scalars().all()
        return order_products

    async def create(self, order_product: OrderProduct) -> OrderProduct:
        try:
            self.session.add(order_product)
            await self.session.commit()
            await self.session.refresh(order_product)
            return order_product
        except Exception as e:
            await self.session.rollback()
            print(f"Error creating order product: {e}")
            raise

    async def create_many(self, order_id: int, order_products: list[OrderProduct]) -> list[OrderProduct]:
        try:
            self.session.add_all(order_products)
            await self.session.commit()
            return await self.get_order_products(order_id)
        except Exception as e:
            await self.session.rollback()
            print(f"Error creating order products: {e}")
            raise

    async def update(self, order_product: OrderProduct) -> OrderProduct:
        try:
            order_product = await self.session.merge(order_product)
            await self.session.commit()
            await self.session.refresh(order_product)
            return order_product
        except Exception as e:
            await self.session.rollback()
            print(f"Error updating order product: {e}")
            raise

    async def delete(self, id: int) -> bool:
        try:
            order_product = await self.session.get(OrderProduct, id)
            await self.session.delete(order_product)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            print(f"Error deleting order product: {e}")
            raise
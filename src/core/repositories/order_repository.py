from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.models import Order, User


class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: int) -> Order | None:
        result = await self.session.execute(select(Order).options(joinedload(Order.user).joinedload(User.role)).
                                            options(joinedload(Order.status)).where(Order.id == id))
        order = result.scalar_one_or_none()
        return order

    async def get_by_user(self, user_id: int) -> Order | None:
        result = await self.session.execute(select(Order).
                                            options(joinedload(Order.user).joinedload(User.role)).
                                            options(joinedload(Order.status)).
                                            where(Order.user_id == user_id))
        order = result.scalar_one_or_none()
        return order

    async def get_user_orders(self, user_id: int) -> list[Order]:
        result = await self.session.execute(select(Order).
                                            options(joinedload(Order.user).joinedload(User.role)).
                                            options(joinedload(Order.status)).
                                            where(Order.user_id == user_id))
        orders = result.scalars().all()
        return orders

    async def get_by_status(self, status_id: int) -> Order | None:
        result = await self.session.execute(select(Order).
                                            options(joinedload(Order.user).joinedload(User.role)).
                                            options(joinedload(Order.status)).
                                            where(Order.status_id == status_id))
        order = result.scalar_one_or_none()
        return order

    async def get_one_by_user_and_status(self, user_id: int, status_id: int) -> Order | None:
        result = await self.session.execute(select(Order).
                                            options(joinedload(Order.user).joinedload(User.role)).
                                            options(joinedload(Order.status)).
                                            where(Order.status_id == status_id, Order.user_id == user_id))
        order = result.scalar_one_or_none()
        return order

    async def get_all_by_user_and_status(self, user_id: int, status_id: int) -> list[Order]:
        result = await self.session.execute(select(Order).
                                            options(joinedload(Order.user).joinedload(User.role)).
                                            options(joinedload(Order.status)).
                                            where(Order.status_id == status_id, Order.user_id == user_id))
        orders = result.scalars().all()
        return orders

    async def get_all(self) -> list[Order]:
        result = await self.session.execute(select(Order).
                                            options(joinedload(Order.user).joinedload(User.role)).
                                            options(joinedload(Order.status)))
        orders = result.scalars().all()
        return orders

    async def create(self, order: Order) -> Order:
        try:
            self.session.add(order)
            await self.session.commit()
            await self.session.refresh(order)
            return order
        except Exception as e:
            await self.session.rollback()
            print(f"Error creating order: {e}")
            raise


    async def update(self, order: Order) -> Order:
        try:
            order = await self.session.merge(order)
            await self.session.commit()
            await self.session.refresh(order)
            return order
        except Exception as e:
            await self.session.rollback()
            print(f"Error updating order: {e}")
            raise

    async def delete(self, id: int) -> bool:
        try:
            order = await self.session.get(Order, id)
            await self.session.delete(order)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            print(f"Error deleting order: {e}")
            raise
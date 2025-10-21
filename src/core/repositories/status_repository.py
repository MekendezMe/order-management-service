from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import OrderStatus


class StatusRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: int) -> OrderStatus | None:
        result = await self.session.execute(select(OrderStatus).where(id == OrderStatus.id))
        status = result.scalar_one_or_none()
        return status

    async def get_by_name(self, name: str) -> OrderStatus | None:
        result = await self.session.execute(select(OrderStatus).where(OrderStatus.name == name))
        status = result.scalar_one_or_none()
        return status

    async def get_all(self) -> list[OrderStatus]:
        result = await self.session.scalars(select(OrderStatus))
        statuses = result.all()
        return statuses

    async def create(self, status: OrderStatus) -> OrderStatus:
        try:
            self.session.add(status)
            await self.session.commit()
            await self.session.refresh(status)
            return status
        except Exception as e:
            await self.session.rollback()
            print(f"Error creating status: {e}")
            raise

    async def update(self, status: OrderStatus) -> OrderStatus:
        try:
            status = await self.session.merge(status)
            await self.session.commit()
            await self.session.refresh(status)
            return status
        except Exception as e:
            await self.session.rollback()
            print(f"Error updating status: {e}")
            raise

    async def delete(self, id: int) -> bool:
        try:
            status = await self.session.get(OrderStatus, id)
            await self.session.delete(status)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            print(f"Error deleting status: {e}")
            raise
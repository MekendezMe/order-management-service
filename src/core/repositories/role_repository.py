from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Role


class RoleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: int) -> Role:
        result = await self.session.execute(select(Role).where(Role.id == id))
        role = result.scalar_one_or_none()
        return role

    async def get_by_name(self, name: str) -> Role:
        result = await self.session.execute(select(Role).where(Role.name == name))
        role = result.scalar_one_or_none()
        return role


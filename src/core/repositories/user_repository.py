from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: int) -> User | None:
        result = await self.session.execute(select(User).options(selectinload(User.role)).where(User.id == id))
        user = result.scalar_one_or_none()
        return user

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(select(User).options(selectinload(User.role)).where(User.email == email))
        user = result.scalar_one_or_none()
        return user

    async def get_all(self) -> list[User]:
        result = await self.session.scalars(select(User))
        users = result.all()
        return users

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





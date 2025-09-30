from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions.user.user import UserExistException, UserNotExistException
from core.models import User
from core.schemas.user import UserRead, UserCreate, UserUpdate

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: int) -> UserRead | None:
        result = await self.session.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()
        return UserRead.model_validate(user) if user else None

    async def get_by_email(self, email: str) -> UserRead | None:
        result = await self.session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        return UserRead.model_validate(user) if user else None

    async def get_all(self) -> list[UserRead]:
        result = await self.session.scalars(select(User))
        users = result.all()
        return [UserRead.model_validate(user) for user in users]

    async def create(self, user_create: UserCreate) -> UserRead:
        try:
            if await self.get_by_email(user_create.email) is not None:
                raise UserExistException()

            user_model = User(**user_create.model_dump())
            self.session.add(user_model)
            await self.session.commit()
            await self.session.refresh(user_model)
            return UserRead.model_validate(user_model)
        except Exception as e:
            await self.session.rollback()
            print(f"Error creating user: {e}")
            raise


    async def update(self, user_update: UserUpdate) -> UserRead:
        try:
            user = await self.session.get(User, user_update.id)
            if not user:
                raise UserNotExistException()

            update_data = user_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(user, field, value)

            await self.session.commit()
            await self.session.refresh(user)
            return UserRead.model_validate(user)
        except Exception as e:
            await self.session.rollback()
            print(f"Error updating user: {e}")
            raise

    async def delete(self, id: int) -> bool:
        user = await self.session.get(User, id)
        if not user:
            return False

        await self.session.delete(user)
        await self.session.commit()
        return True





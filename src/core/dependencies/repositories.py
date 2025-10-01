from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.db_helper import db_helper
from core.repositories.role_repository import RoleRepository
from core.repositories.user_repository import UserRepository


async def get_user_repository(
        session: AsyncSession = Depends(db_helper.session_getter)
) -> UserRepository:
    return UserRepository(session)

async def get_role_repository(
        session: AsyncSession = Depends(db_helper.session_getter)
) -> RoleRepository:
    return RoleRepository(session)
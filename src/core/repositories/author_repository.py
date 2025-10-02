from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Author


class AuthorRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: int) -> Author | None:
        result = await self.session.execute(select(Author).where(id == Author.id))
        author = result.scalar_one_or_none()
        return author

    async def get_by_name(self, name: str) -> Author | None:
        result = await self.session.execute(select(Author).where(Author.name == name))
        author = result.scalar_one_or_none()
        return author

    async def get_all(self) -> list[Author]:
        result = await self.session.scalars(select(Author))
        authors = result.all()
        return authors
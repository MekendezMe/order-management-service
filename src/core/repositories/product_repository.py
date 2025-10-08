from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import Product


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: int) -> Product | None:
        result = await self.session.execute(select(Product).options(selectinload(Product.author)).where(Product.id == id))
        product = result.scalar_one_or_none()
        return product

    async def get_by_article(self, article: str) -> Product | None:
        result = await self.session.execute(select(Product).options(selectinload(Product.author)).where(Product.article == article))
        product = result.scalar_one_or_none()
        return product

    async def get_all(self) -> list[Product]:
        result = await self.session.scalars(select(Product))
        products = result.all()
        return products

    async def create(self, product: Product) -> Product:
        try:
            self.session.add(product)
            await self.session.commit()
            await self.session.refresh(product)
            return product
        except Exception as e:
            await self.session.rollback()
            print(f"Error creating product: {e}")
            raise


    async def update(self, product: Product) -> Product:
        try:
            await self.session.commit()
            await self.session.refresh(product)
            return product
        except Exception as e:
            await self.session.rollback()
            print(f"Error updating product: {e}")
            raise

    async def delete(self, id: int) -> bool:
        try:
            product = await self.session.get(Product, id)
            await self.session.delete(product)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            print(f"Error updating product: {e}")
            raise
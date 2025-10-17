
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.exceptions.product import NotEnoughStockException
from core.models import Product
from core.repositories.helpers.pagination_params import PaginationParams
from core.repositories.helpers.sort_params import SortParams
from core.schemas.product import ProductQuantity
from core.schemas.product_filters import ProductFilter


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: int) -> Product | None:
        result = await self.session.execute(select(Product).options(selectinload(Product.author))
                                            .where(Product.id == id))
        product = result.scalar_one_or_none()
        return product

    async def get_by_article(self, article: str) -> Product | None:
        result = await self.session.execute(select(Product).options(selectinload(Product.author))
                                            .where(Product.article == article))
        product = result.scalar_one_or_none()
        return product

    async def get_all(self) -> list[Product]:
        result = await self.session.scalars(select(Product))
        products = result.all()
        return products

    async def get_with_filters_sorted_paginated(
            self, product_filter: ProductFilter,
            pagination_params: PaginationParams,
            sort_params: SortParams
    ) -> list[Product]:
        try:
            query = select(Product).options(selectinload(Product.author))

            if product_filter.min_price is not None:
                query = query.where(Product.price >= product_filter.min_price)

            if product_filter.max_price is not None:
                query = query.where(Product.price <= product_filter.max_price)

            if product_filter.min_age is not None:
                query = query.where(Product.minimal_age >= product_filter.min_age)

            if product_filter.in_stock_only:
                query = query.where(Product.stock_quantity > 0)

            if product_filter.author_id is not None:
                query = query.where(Product.author_id == product_filter.author_id)

            query = query.order_by(getattr(Product, sort_params.sort_by).asc()
                                   if sort_params.sort_order == "asc"
                                   else getattr(Product, sort_params.sort_by).desc())

            query = query.limit(pagination_params.limit).offset(pagination_params.offset)

            result = await self.session.execute(query)
            return result.scalars().all()
        except Exception as e:
            print("Error get products:", e)
            raise


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
            product = await self.session.merge(product)
            await self.session.commit()
            await self.session.refresh(product)
            updated_product = await self.get_by_id(product.id)
            return updated_product
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
            print(f"Error deleting product: {e}")
            raise

    async def reserve_all(self, product_quantities: list[ProductQuantity]) -> bool:
        try:
            async with self.session.begin():
                for product_quantity in product_quantities:
                    product = await self.session.get(Product, product_quantity.product_id,
                                                     with_for_update=True)

                    if product is None or product.stock_quantity < product_quantity.quantity:
                        raise NotEnoughStockException(f"Товара {product.name} недостаточно на складе, доступно лишь {product.stock_quantity} шт.")

                    product.stock_quantity -= product_quantity.quantity

                return True
        except NotEnoughStockException:
            await self.session.rollback()
            return False
import random
import string
from typing import Union, Optional

from api.query_params.product_query_params import ProductQueryParams
from core.constants import MAX_AGE
from core.exceptions.product import IncorrectAgeException, IncorrectNumberException, ProductNotFoundException
from core.exceptions.author import AuthorNotFoundException
from core.repositories.author_repository import AuthorRepository
from core.repositories.product_repository import ProductRepository
from core.schemas.product import ProductCreate, ProductRead, ProductUpdate
from core.services.mappers.product_mapper import create_to_model, model_to_read, update_to_model


def generate_article() -> str:
    length = random.randint(3, 8)
    first_digit = random.randint(1, 9)
    other_digits = ''.join(random.choice(string.digits) for _ in range(length - 1))
    return str(first_digit) + other_digits


class ProductService:
    def __init__(self, product_repository: ProductRepository, author_repository: AuthorRepository):
        self.product_repository = product_repository
        self.author_repository = author_repository

    async def get(self, params: ProductQueryParams):
        if params.product_filter.author_id is not None:
            author = await self.author_repository.get_by_id(params.product_filter.author_id)
            if author is None:
                raise AuthorNotFoundException()


        products = await (self.product_repository
                      .get_with_filters_sorted_paginated(params.product_filter,
                                                         pagination_params=params.pagination_params,
                                                         sort_params=params.sort_params))

        products_read = [model_to_read(product) for product in products]
        return products_read

    async def create(self, product_create: ProductCreate) -> ProductRead:
        _validate_product_data(product_create)

        author = await self.author_repository.get_by_id(product_create.author_id)
        if not author:
            raise AuthorNotFoundException()

        article = generate_article()
        product = create_to_model(product_create, article, author.id)
        created_product = await self.product_repository.create(product)

        return model_to_read(created_product)

    async def update(self, id: int, product_update: ProductUpdate):
        _validate_product_data(product_update)

        existed_product = await self.product_repository.get_by_id(id)
        if not existed_product:
            raise ProductNotFoundException()

        product = update_to_model(product_update, id, article=existed_product.article)
        updated_product = await self.product_repository.update(product)

        return model_to_read(updated_product)

    async def delete(self, id: int):
        product = await self.product_repository.get_by_id(id)
        if not product:
            raise ProductNotFoundException()

        return await self.product_repository.delete(id)


def _validate_product_data(
        product_data: Union[ProductCreate, ProductUpdate],
):
    if not 0 <= product_data.minimal_age <= MAX_AGE:
        raise IncorrectAgeException()
    if product_data.price < 0 or product_data.discount_price < 0:
        raise IncorrectNumberException("Цена должна быть положительной")
    if product_data.discount_price > product_data.price:
        raise IncorrectNumberException("Цена со скидкой должна быть меньше цены без скидки")
    if product_data.stock_quantity < 0:
        raise IncorrectNumberException("Количество на складе должно быть положительным")
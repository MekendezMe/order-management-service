import random
import string

from core.constants import MAX_AGE
from core.exceptions.product import IncorrectAgeException, IncorrectNumberException
from core.exceptions.author import AuthorNotFoundException
from core.repositories.author_repository import AuthorRepository
from core.repositories.product_repository import ProductRepository
from core.schemas.product import ProductCreate, ProductRead
from core.services.mappers.product_mapper import create_to_model, model_to_read


def generate_article() -> str:
    length = random.randint(3, 8)
    first_digit = random.randint(1, 9)
    other_digits = ''.join(random.choice(string.digits) for _ in range(length - 1))
    return str(first_digit) + other_digits


class ProductService:
    def __init__(self, product_repository: ProductRepository, author_repository: AuthorRepository):
        self.product_repository = product_repository
        self.author_repository = author_repository

    async def create(self, product_create: ProductCreate) -> ProductRead:
        if not 0 <= product_create.minimal_age <= MAX_AGE:
            raise IncorrectAgeException()
        if product_create.price < 0 or product_create.discount_price < 0:
            raise IncorrectNumberException("Цена должна быть положительной")
        if product_create.discount_price > product_create.price:
            raise IncorrectNumberException("Цена со скидкой должна быть меньше цены без скидки")
        if product_create.stock_quantity < 0:
            raise IncorrectNumberException("Количество на складе должно быть положительным")
        author = await self.author_repository.get_by_name(product_create.author)
        if not author:
            raise AuthorNotFoundException()

        article = generate_article()
        product = create_to_model(product_create, article, author.id)
        created_product = await self.product_repository.create(product)

        return model_to_read(created_product)


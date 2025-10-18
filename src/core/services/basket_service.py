import decimal

from core.exceptions.basket import IncorrectCountException, BasketNotFoundException
from core.exceptions.product import ProductNotFoundException
from core.exceptions.user import UserNotFoundException
from core.models import BasketProduct
from core.repositories.basket_repository import BasketRepository
from core.repositories.product_repository import ProductRepository
from core.repositories.user_repository import UserRepository
from core.schemas.basket import BasketRead, BasketCreate, BasketItem, BasketForUserResponse, BasketTotal
from core.services.mappers.basket_mapper import create_to_model, model_to_read, model_to_get_one_from_user, \
    model_to_get_all_from_user


class BasketService:
    def __init__(self,
                 basket_repository: BasketRepository,
                 user_repository: UserRepository,
                 product_repository: ProductRepository):
        self.basket_repository = basket_repository
        self.user_repository = user_repository
        self.product_repository = product_repository

    async def add(self, basket_create: BasketCreate) -> BasketRead:
        _validate_basket_data(basket_create.count)

        user = await self.user_repository.get_by_id(basket_create.user_id)
        if not user:
            raise UserNotFoundException(f"Пользователь с id {basket_create.user_id} не существует")

        product = await self.product_repository.get_by_id(basket_create.product_id)
        if not product:
            raise ProductNotFoundException(f"Продукт с id {basket_create.product_id} не существует")

        product_in_basket = await (self.basket_repository.
                                   get_by_user_and_product(basket_create.user_id,
                                                           basket_create.product_id))
        if product_in_basket:
            product_in_basket.count = product_in_basket.count + basket_create.count
            updated_basket = await self.basket_repository.update(product_in_basket)
            return model_to_read(updated_basket)
        else:
            basket = create_to_model(basket_create)
            created_basket = await self.basket_repository.create(basket)
            return model_to_read(created_basket)

    async def update(self, id: int, count: int):
        _validate_basket_data(count)

        existed_basket = await self.basket_repository.get_by_id(id)
        if not existed_basket:
            raise BasketNotFoundException()

        existed_basket.count = count
        updated_basket = await self.basket_repository.update(existed_basket)

        return model_to_read(updated_basket)

    async def delete(self, id: int):
        basket = await self.basket_repository.get_by_id(id)
        if not basket:
            raise BasketNotFoundException()

        return await self.basket_repository.delete(id)

    async def delete_basket_item(self, basket_item: BasketItem):
        user = await self.user_repository.get_by_id(basket_item.user_id)
        if not user:
            raise UserNotFoundException(f"Пользователь с id {basket_item.user_id} не существует")

        product = await self.product_repository.get_by_id(basket_item.product_id)
        if not product:
            raise ProductNotFoundException(f"Продукт с id {basket_item.product_id} не существует")

        user_item = await self.basket_repository.get_by_user_and_product(basket_item.user_id, basket_item.product_id)

        if not user_item:
            raise BasketNotFoundException()

        return await self.basket_repository.clear_item_in_user_basket(basket_item.user_id, basket_item.product_id)


    async def get_user_items(self, user_id: int):

        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"Пользователь с id {user_id} не существует")

        user_items = await self.basket_repository.get_user_items(user_id)


        items_without_user = []
        for item in user_items:
            items_without_user.append(model_to_get_one_from_user(item))

        items_without_user = [model_to_get_one_from_user(item) for item in user_items]

        total_data = _get_total_data(user_items)

        return model_to_get_all_from_user(
            user=user,
            items=items_without_user,
            total=total_data
        )


def _validate_basket_data(
        count: int,
):
    if count <= 0:
        raise IncorrectCountException()


def _get_total_data(user_items: list[BasketProduct]) -> BasketTotal:
    price = decimal.Decimal(0)
    discount_price = decimal.Decimal(0)
    total_saved = decimal.Decimal(0)
    count: int = 0
    for item in user_items:
        if not item.product or not item.product.is_active:
            continue

        price += item.product.price * item.count
        discount_price += item.product.discount_price * item.count
        count += item.count

    total_saved = price - discount_price

    return BasketTotal(
        price=price,
        discount_price=discount_price,
        count=count,
        total_saved=total_saved
    )
from core.models import BasketProduct, User
from core.schemas.basket import BasketRead, BasketCreate, BasketForUserResponse, BasketItemWithoutUser, BasketTotal
from core.services.mappers import user_mapper, product_mapper


def model_to_read(basket: BasketProduct) -> BasketRead:
    return BasketRead(
        id=basket.id,
        user=user_mapper.model_to_read(basket.user),
        product=product_mapper.model_to_read(basket.product),
        count=basket.count
    )

def create_to_model(basket_create: BasketCreate) -> BasketProduct:
    return BasketProduct(
        user_id=basket_create.user_id,
        product_id=basket_create.product_id,
        count=basket_create.count
    )

def model_to_get_one_from_user(basket: BasketProduct) -> BasketItemWithoutUser:
    return BasketItemWithoutUser(
        id=basket.id,
        product=product_mapper.model_to_read(basket.product),
        count=basket.count
    )

def model_to_get_all_from_user(
        user: User,
        items: list[BasketItemWithoutUser],
        total: BasketTotal
) -> BasketForUserResponse:
    return BasketForUserResponse(
        user=user_mapper.model_to_read(user),
        items=items,
        total=total
    )
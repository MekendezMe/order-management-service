import decimal

from core.constants import STATUS_CREATED_ID
from core.models import Order
from core.schemas.order import OrderRead, OrderWithProducts, OrderProductWithoutOrderId
from core.services.mappers import user_mapper, status_mapper


def model_to_read(order: Order) -> OrderRead:
    return OrderRead(
        id=order.id,
        user=user_mapper.model_to_read(order.user),
        count=order.count_products,
        price=order.price,
        status=status_mapper.model_to_read(order.status)
    )

def models_to_read(orders: list[Order]) -> list[OrderRead]:
    return [model_to_read(order) for order in orders]


def create_to_model(user_id: int, count: int, price: decimal.Decimal) -> Order:
    return Order(
        user_id=user_id,
        count_products=count,
        price=price,
        status_id=STATUS_CREATED_ID
    )

def model_to_order_with_products(order: OrderRead, products: list[OrderProductWithoutOrderId]):
    return OrderWithProducts(
        order=order,
        products=products
    )

from core.models import OrderProduct
from core.schemas.order import OrderProductWithoutOrderId
from core.services.mappers import product_mapper


def model_to_read_without_order_id(order_product: OrderProduct) -> OrderProductWithoutOrderId:
    return OrderProductWithoutOrderId(
        id=order_product.id,
        product=product_mapper.model_to_read(order_product.product),
        count=order_product.count,
        price=order_product.price
    )

def models_to_read_without_order_id(order_products: list[OrderProduct]) -> list[OrderProductWithoutOrderId]:
    products: list[OrderProductWithoutOrderId] = [model_to_read_without_order_id(product)
                                                  for product in order_products]
    return products

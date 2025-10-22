import decimal

from core.exceptions.basket import BasketNotFoundException
from core.exceptions.order import OrderNotFoundException
from core.exceptions.order_product import OrderProductCreateManyException
from core.exceptions.product import ProductNotFoundException, NotEnoughStockException
from core.exceptions.status import StatusNotFoundException
from core.exceptions.user import UserNotFoundException
from core.models import OrderProduct
from core.repositories.basket_repository import BasketRepository
from core.repositories.order_product_repository import OrderProductRepository
from core.repositories.order_repository import OrderRepository
from core.repositories.product_repository import ProductRepository
from core.repositories.status_repository import StatusRepository
from core.repositories.user_repository import UserRepository
from core.schemas.order import OrderCreate, OrderRead, OrderItemCreate, OrderWithProducts
from core.services.mappers.order_mapper import create_to_model, model_to_read, model_to_order_with_products, \
    models_to_read
from core.services.mappers.order_product_mapper import models_to_read_without_order_id


class OrderService:
    def __init__(self,
                 basket_repository: BasketRepository,
                 user_repository: UserRepository,
                 order_repository: OrderRepository,
                 product_repository: ProductRepository,
                 status_repository: StatusRepository,
                 order_product_repository: OrderProductRepository):
        self.basket_repository = basket_repository
        self.user_repository = user_repository
        self.order_repository = order_repository
        self.product_repository = product_repository
        self.status_repository = status_repository
        self.order_product_repository = order_product_repository

    async def create(self, order_create: OrderCreate) -> OrderWithProducts:
        user = await self.user_repository.get_by_id(order_create.user_id)
        if not user:
            raise UserNotFoundException(f"Пользователь с id {order_create.user_id} не существует")

        total_price = decimal.Decimal(0)
        total_count: int = 0

        for item in order_create.items:
            product = await self.product_repository.get_by_id(item.product_id)
            if not product:
                raise ProductNotFoundException(f"Продукт с id {item.product_id} не существует")
            if product.stock_quantity < item.count:
                raise NotEnoughStockException()
            if await self.basket_repository.get_by_user_and_product(order_create.user_id, item.product_id) is None:
                raise BasketNotFoundException()
            total_price += product.discount_price
            total_count += item.count


        order = create_to_model(order_create.user_id, price=total_price, count=total_count)
        created_order = await self.order_repository.create(order)
        order_products: list[OrderProduct] = []

        for item in order_create.items:
            order_item = OrderProduct(
                order_id=created_order.id,
                product_id=item.product_id,
                count=item.count,
                price=item.price
            )
            order_products.append(order_item)

        created_order_products = await self.order_product_repository.create_many(created_order.id, order_products)
        if not created_order_products:
            raise OrderProductCreateManyException()

        converted_order_products = models_to_read_without_order_id(created_order_products)

        order_with_user = await self.order_repository.get_by_id(created_order.id)
        converted_order = model_to_read(order_with_user)

        return model_to_order_with_products(converted_order, converted_order_products)



    async def update(self, id: int, status_id: int) -> OrderRead:

        existed_order = await self.order_repository.get_by_id(id)
        if not existed_order:
            raise OrderNotFoundException()

        existed_status = await self.status_repository.get_by_id(status_id)
        if not existed_status:
            raise StatusNotFoundException()

        existed_order.status_id = status_id
        updated_order = await self.order_repository.update(existed_order)

        return model_to_read(updated_order)


    async def delete(self, id: int) -> bool:
        order = await self.order_repository.get_by_id(id)
        if not order:
            raise OrderNotFoundException()

        return await self.order_repository.delete(id)

    async def get_one(self, id: int) -> OrderWithProducts:
        order = await self.order_repository.get_by_id(id)
        if not order:
            raise OrderNotFoundException()

        order_products = await self.order_product_repository.get_order_products(id)

        converted_order_products = models_to_read_without_order_id(order_products)

        converted_order = model_to_read(order)

        return model_to_order_with_products(converted_order, converted_order_products)


    async def get_all_by_user(self, user_id: int) -> list[OrderWithProducts]:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"Пользователь с id {user_id} не существует")

        orders = await self.order_repository.get_user_orders(user_id)

        converted_orders = models_to_read(orders)

        order_with_products: list[OrderWithProducts] = []

        for order in converted_orders:
            order_products = await self.order_product_repository.get_order_products(order.id)
            converted_order_products = models_to_read_without_order_id(order_products)
            order_with_products.append(OrderWithProducts(
                order=order,
                products=converted_order_products
            ))

        return order_with_products
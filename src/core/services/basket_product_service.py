from core.repositories.basket_product_repository import BasketProductRepository


class BasketProductService:
    def __init__(self, basket_product_repository: BasketProductRepository):
        self.basket_product_repository = basket_product_repository
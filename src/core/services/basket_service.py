from core.repositories.basket_repository import BasketRepository


class BasketService:
    def __init__(self, basket_repository: BasketRepository):
        self.basket_repository = basket_repository


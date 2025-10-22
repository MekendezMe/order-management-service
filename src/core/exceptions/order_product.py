class OrderProductCreateManyException(Exception):
    def __init__(self, message: str = "Ошибка создания нескольких товаров"):
        super().__init__(message)
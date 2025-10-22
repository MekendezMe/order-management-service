class OrderProductCreateManyException(Exception):
    def __init__(self, message: str = "Ошибка создания нескольких товаров"):
        super().__init__(message)

class OrderProductDeleteManyException(Exception):
    def __init__(self, message: str = "Ошибка удаления нескольких товаров"):
        super().__init__(message)
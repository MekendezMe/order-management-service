class IncorrectAgeException(Exception):
    def __init__(self, message: str = "Возрастной диапазон товара должен быть от 0 до 18"):
        super().__init__(message)

class IncorrectNumberException(Exception):
    def __init__(self, message: str = "Значение должно быть положительным"):
        super().__init__(message)

class ProductNotFoundException(Exception):
    def __init__(self, message: str = "Продукт с указанным id не найден"):
        super().__init__(message)

class NotEnoughStockException(Exception):
    def __init__(self, message: str = "Недостаточно товара на складе"):
        super().__init__(message)

class LowAgeException(Exception):
    def __init__(self, message: str = "Неподходящий возраст под выбранный товар"):
        super().__init__(message)
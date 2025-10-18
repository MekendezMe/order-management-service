class IncorrectCountException(Exception):
    def __init__(self, message: str = "Количество должно быть больше нуля"):
        super().__init__(message)


class BasketNotFoundException(Exception):
    def __init__(self, message: str = "Товар в корзине указанным id не найден"):
        super().__init__(message)
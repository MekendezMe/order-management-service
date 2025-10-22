class OrderNotFoundException(Exception):
    def __init__(self, message: str = "Заказ с указанным id не найден"):
        super().__init__(message)
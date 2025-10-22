class StatusNotFoundException(Exception):
    def __init__(self, message: str = "Статус заказа с указанным id не найден"):
        super().__init__(message)
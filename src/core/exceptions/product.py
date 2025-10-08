class IncorrectAgeException(Exception):
    def __init__(self, message: str = "Возрастной диапазон товара должен быть от 0 до 18"):
        super().__init__(message)

class IncorrectNumberException(Exception):
    def __init__(self, message: str = "Значение должно быть положительным"):
        super().__init__(message)
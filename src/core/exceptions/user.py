class UserAlreadyExistException(Exception):
    def __init__(self, message: str = "Пользователь с указанным email уже существует"):
        super().__init__(message)


class UserNotFoundException(Exception):
    def __init__(self, message: str = "Пользователь с указанным email не существует"):
        super().__init__(message)

class InvalidPasswordLengthException(Exception):
    def __init__(self, message: str = "Минимальная длина пароля - 8 символов"):
        super().__init__(message)

class IncorrectPasswordException(Exception):
    def __init__(self, message: str = "Указан неверный пароль"):
        super().__init__(message)
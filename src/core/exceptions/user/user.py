class UserExistException(Exception):
    def __init__(self, message: str = "Пользователь с указанным email уже существует"):
        super().__init__(message)


class UserNotExistException(Exception):
    def __init__(self, message: str = "Пользователь с указанным email не существует"):
        super().__init__(message)
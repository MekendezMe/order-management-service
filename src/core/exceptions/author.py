class AuthorNotFoundException(Exception):
    def __init__(self, message: str = "Автор с указанным id не существует"):
        super().__init__(message)
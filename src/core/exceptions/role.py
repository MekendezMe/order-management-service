class RoleNotFoundException(Exception):
    def __init__(self, message: str = "Роль с указанным name не найдена"):
        super().__init__(message)
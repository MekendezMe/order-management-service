from core.models import User, Role
from core.schemas.user import UserRead, UserCreate


def model_to_read(user: User) -> UserRead:
    return UserRead(
        id=user.id,
        email=user.email,
        name=user.name,
        surname=user.surname,
        age=user.age,
        role=user.role.name,
        confirmed=user.confirmed,
        is_active=user.is_active
    )

def create_to_model(user_create: UserCreate, hashed_password: str, role: Role) -> User:
    return User(
        email=user_create.email,
        password=hashed_password,
        name=user_create.name,
        surname=user_create.surname,
        age=user_create.age,
        role_id=role.id,
    )

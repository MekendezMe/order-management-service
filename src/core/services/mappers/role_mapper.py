from core.models import Role
from core.schemas.role import RoleRead


def model_to_read(role: Role) -> RoleRead:
    return RoleRead(
        id=role.id,
        name=role.name
    )
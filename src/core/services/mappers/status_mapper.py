from core.models import OrderStatus
from core.schemas.status import StatusRead


def model_to_read(status: OrderStatus) -> StatusRead:
    return StatusRead(
        id=status.id,
        name=status.name
    )
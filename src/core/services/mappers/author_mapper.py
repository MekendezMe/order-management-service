from core.models import Author
from core.schemas.author import AuthorRead


def model_to_read(author: Author) -> AuthorRead:
    return AuthorRead(
        id=author.id,
        name=author.name,
        verified=author.verified
    )
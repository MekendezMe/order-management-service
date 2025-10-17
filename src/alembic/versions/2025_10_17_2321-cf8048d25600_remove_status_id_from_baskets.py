"""remove_status_id_from_baskets

Revision ID: cf8048d25600
Revises: de4d8466beb5
Create Date: 2025-10-17 23:21:50.482633

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cf8048d25600"
down_revision: Union[str, Sequence[str], None] = "de4d8466beb5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

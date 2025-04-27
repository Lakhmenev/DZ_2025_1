"""update users

Revision ID: 9b5fc242d747
Revises: 3e98b1fde329
Create Date: 2025-04-27 16:08:01.909079

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9b5fc242d747"
down_revision: Union[str, None] = "3e98b1fde329"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, "users", ["email"])
    op.create_unique_constraint(None, "users", ["nickname"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "users", type_="unique")
    op.drop_constraint(None, "users", type_="unique")


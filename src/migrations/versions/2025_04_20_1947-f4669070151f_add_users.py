"""add users

Revision ID: f4669070151f
Revises: 18a91921a323
Create Date: 2025-04-20 19:47:34.444917

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f4669070151f"
down_revision: Union[str, None] = "18a91921a323"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.Column("Nickname", sa.String(length=100), nullable=False),
        sa.Column("Firstname", sa.String(length=100), nullable=False),
        sa.Column("Lastname", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("users")

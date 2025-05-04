"""edit users

Revision ID: 3e98b1fde329
Revises: f4669070151f
Create Date: 2025-04-20 23:33:22.925869

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3e98b1fde329"
down_revision: Union[str, None] = "f4669070151f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("nickname", sa.String(length=100), nullable=False))
    op.add_column(
        "users", sa.Column("firstname", sa.String(length=100), nullable=False)
    )
    op.add_column("users", sa.Column("lastname", sa.String(length=100), nullable=False))
    op.drop_column("users", "Lastname")
    op.drop_column("users", "Firstname")
    op.drop_column("users", "Nickname")



def downgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "Nickname", sa.VARCHAR(length=100), autoincrement=False, nullable=False
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "Firstname", sa.VARCHAR(length=100), autoincrement=False, nullable=False
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "Lastname", sa.VARCHAR(length=100), autoincrement=False, nullable=False
        ),
    )
    op.drop_column("users", "lastname")
    op.drop_column("users", "firstname")
    op.drop_column("users", "nickname")


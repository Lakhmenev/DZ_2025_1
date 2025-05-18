"""update rooms

Revision ID: 672a0160887d
Revises: 9b5fc242d747
Create Date: 2025-05-18 14:52:52.181054

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "672a0160887d"
down_revision: Union[str, None] = "9b5fc242d747"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("rooms", sa.Column("hotel_id", sa.Integer(), nullable=False))
    op.drop_constraint("rooms_hostel_id_fkey", "rooms", type_="foreignkey")
    op.create_foreign_key(None, "rooms", "hotels", ["hotel_id"], ["id"])
    op.drop_column("rooms", "hostel_id")


def downgrade() -> None:
    op.add_column(
        "rooms",
        sa.Column("hostel_id", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(None, "rooms", type_="foreignkey")
    op.create_foreign_key(
        "rooms_hostel_id_fkey", "rooms", "hotels", ["hostel_id"], ["id"]
    )
    op.drop_column("rooms", "hotel_id")

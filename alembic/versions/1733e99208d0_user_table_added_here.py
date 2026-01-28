"""user table added here

Revision ID: 1733e99208d0
Revises: b654a5217517
Create Date: 2026-01-28 01:49:07.518272

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1733e99208d0'
down_revision: Union[str, Sequence[str], None] = 'b654a5217517'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    def upgrade():
        op.create_table(
            "users",
            sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
            sa.Column("name", sa.String(), nullable=False),
            sa.Column("username", sa.String(), nullable=False),
            sa.Column("email", sa.String(), nullable=False),
            sa.Column(
                "created_at",
                sa.TIMESTAMP(timezone=True),
                server_default=sa.text("now()"),
                nullable=False,
            ),
            sa.Column("phone_no", sa.String(15), nullable=True),

            sa.UniqueConstraint("username"),
            sa.UniqueConstraint("email"),
        )

        op.create_index("ix_users_username", "users", ["username"])
        op.create_index("ix_users_email", "users", ["email"])

    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass

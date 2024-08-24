"""add user table

Revision ID: acd1e3269c55
Revises: 88bd9822fb07
Create Date: 2024-08-24 15:44:41.973882

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'acd1e3269c55'
down_revision: Union[str, None] = '88bd9822fb07'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), 
                  server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint('email'),
        sa.PrimaryKeyConstraint('id')
    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass

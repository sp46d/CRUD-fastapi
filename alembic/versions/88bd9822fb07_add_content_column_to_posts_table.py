"""add content column to posts table

Revision ID: 88bd9822fb07
Revises: f07a4072c9b8
Create Date: 2024-08-24 15:30:59.381399

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '88bd9822fb07'
down_revision: Union[str, None] = 'f07a4072c9b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('content', sa.String(), nullable=False)
    )
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass

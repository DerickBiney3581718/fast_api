import sqlmodel
"""add nickname column to users

Revision ID: 3d49849d46cb
Revises: 2e434959bbe3
Create Date: 2024-11-08 15:47:51.616202

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d49849d46cb'
down_revision: Union[str, None] = '2e434959bbe3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users',
    sa.Column('nickname',sa.Text(), nullable=True ))


def downgrade() -> None:
    op.drop_column('users',
    'nickname')
    pass

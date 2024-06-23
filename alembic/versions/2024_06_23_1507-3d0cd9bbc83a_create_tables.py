"""create tables

Revision ID: 3d0cd9bbc83a
Revises: 959804819e0b
Create Date: 2024-06-23 15:07:50.955830

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d0cd9bbc83a'
down_revision: Union[str, None] = '959804819e0b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dealer', sa.Column('address', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'dealer', ['address'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'dealer', type_='unique')
    op.drop_column('dealer', 'address')
    # ### end Alembic commands ###

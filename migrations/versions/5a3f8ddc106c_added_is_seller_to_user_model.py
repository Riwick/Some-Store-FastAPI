"""added is_seller to user model

Revision ID: 5a3f8ddc106c
Revises: 7e1c92a0e372
Create Date: 2024-03-09 11:46:57.427494

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a3f8ddc106c'
down_revision: Union[str, None] = '7e1c92a0e372'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_seller', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'is_seller')
    # ### end Alembic commands ###
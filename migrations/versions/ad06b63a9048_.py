"""empty message

Revision ID: ad06b63a9048
Revises: 
Create Date: 2023-09-04 01:00:50.996289

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ad06b63a9048'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('title',
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('vector', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('title')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('title')
    # ### end Alembic commands ###

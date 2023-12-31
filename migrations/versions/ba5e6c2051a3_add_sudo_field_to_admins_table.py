"""Add sudo field to admins table

Revision ID: ba5e6c2051a3
Revises: 0d835f43dec6
Create Date: 2023-12-20 17:29:21.651337

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba5e6c2051a3'
down_revision: Union[str, None] = '0d835f43dec6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('admins', sa.Column('sudo', sa.Boolean(), server_default='0', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('admins', 'sudo')
    # ### end Alembic commands ###

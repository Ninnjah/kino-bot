"""Update films tables

Revision ID: 9f3feb6e011b
Revises: 5d5b7183fc2a
Create Date: 2023-12-06 00:47:23.409409

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '9f3feb6e011b'
down_revision: Union[str, None] = '5d5b7183fc2a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('films',
    sa.Column('film_id', sa.Integer(), nullable=False),
    sa.Column('name_ru', sa.String(), nullable=True),
    sa.Column('name_en', sa.String(), nullable=True),
    sa.Column('type', postgresql.ENUM('FILM', 'film', 'TV_SHOW', 'TV_SERIES', 'SERIES', 'CARTOON_SERIES', 'MINI_SERIES', 'VIDEO', 'UNKNOWN', name='filmtype'), nullable=True),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('film_length', sa.String(), nullable=True),
    sa.Column('countries', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('genres', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('rating', sa.String(), nullable=True),
    sa.Column('rating_vote_count', sa.Integer(), nullable=True),
    sa.Column('poster_url', sa.String(), nullable=True),
    sa.Column('poster_url_preview', sa.String(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('updated_on', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('film_id')
    )
    op.create_table('sources',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('film_id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('updated_on', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['film_id'], ['films.film_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sources')
    op.drop_table('films')
    # ### end Alembic commands ###
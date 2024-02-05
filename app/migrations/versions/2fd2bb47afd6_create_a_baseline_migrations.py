"""Create a baseline migrations

Revision ID: 2fd2bb47afd6
Revises: 
Create Date: 2024-02-05 01:54:42.060812

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2fd2bb47afd6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tournaments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('matchs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('left_player_name', sa.String(), nullable=True),
    sa.Column('right_player_name', sa.String(), nullable=True),
    sa.Column('winner', sa.String(), nullable=True),
    sa.Column('loser', sa.String(), nullable=True),
    sa.Column('final_match', sa.Boolean(), nullable=False),
    sa.Column('third_place', sa.Boolean(), nullable=False),
    sa.Column('left_previous_match_id', sa.Integer(), nullable=True),
    sa.Column('right_previous_match_id', sa.Integer(), nullable=True),
    sa.Column('tournament_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['left_previous_match_id'], ['matchs.id'], ),
    sa.ForeignKeyConstraint(['right_previous_match_id'], ['matchs.id'], ),
    sa.ForeignKeyConstraint(['tournament_id'], ['tournaments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('matchs')
    op.drop_table('tournaments')
    # ### end Alembic commands ###
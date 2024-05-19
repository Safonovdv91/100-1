"""add admin_game_id

Revision ID: d1a6b0292541
Revises: be6971b4d0cf
Create Date: 2024-05-19 07:59:17.635793

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1a6b0292541'
down_revision: Union[str, None] = 'be6971b4d0cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('games', sa.Column('admin_game_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('games', 'admin_game_id')
    # ### end Alembic commands ###

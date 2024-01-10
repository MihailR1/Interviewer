"""empty message

Revision ID: 1cef056f0756
Revises: 96dfd42a9aa8
Create Date: 2024-01-10 17:23:16.978903

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '1cef056f0756'
down_revision: Union[str, None] = '96dfd42a9aa8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_Questions_title', table_name='Questions')
    op.create_index(op.f('ix_Questions_title'), 'Questions', ['title'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_Questions_title'), table_name='Questions')
    op.create_index('ix_Questions_title', 'Questions', ['title'], unique=False)
    # ### end Alembic commands ###
"""Volver columna

Revision ID: 63401f204cca
Revises: cb5079494032
Create Date: 2022-10-16 10:19:18.575678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63401f204cca'
down_revision = 'cb5079494032'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('usuario', sa.Column('estado', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('usuario', 'estado')
    # ### end Alembic commands ###

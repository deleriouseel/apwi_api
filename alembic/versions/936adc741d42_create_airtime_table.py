"""create airtime table

Revision ID: 936adc741d42
Revises: 8b7bbe8f62dd
Create Date: 2022-10-14 15:10:12.548463

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '936adc741d42'
down_revision = '8b7bbe8f62dd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('airtime', sa.Column('idAirtime', sa.Integer(), nullable=False, primary_key=True, autoincrement=True ), sa.Column('time', sa.Time(), nullable=False), sa.Column('airdays', sa.String(), nullable=False), sa.Column('live', sa.Integer, nullable=False, default=0), sa.UniqueConstraint('idAirtime'))
    pass


def downgrade() -> None:
    op.drop_table('airtime')
    pass

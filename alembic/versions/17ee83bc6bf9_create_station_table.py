"""create station table

Revision ID: 17ee83bc6bf9
Revises: 936adc741d42
Create Date: 2022-10-20 10:05:46.143017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17ee83bc6bf9'
down_revision = '936adc741d42'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('station', sa.Column('idStation', sa.Integer(), nullable=False, primary_key=True, autoincrement=True ), sa.Column('callLetters', sa.String(), nullable=False), sa.Column('network', sa.String(), nullable=False), sa.UniqueConstraint('idStation'))
    pass


def downgrade() -> None:
    op.drop_table('station')
    pass

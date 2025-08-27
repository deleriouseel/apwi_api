"""add columns to station table

Revision ID: 319454195733
Revises: baa952621d49
Create Date: 2025-08-27 14:19:14.199318

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '319454195733'
down_revision = 'baa952621d49'
branch_labels = None
depends_on = None


def upgrade():
    # Add the missing columns without foreign keys
    op.add_column('station', sa.Column('frequency', sa.String(), nullable=True))
    op.add_column('station', sa.Column('location', sa.Integer(), nullable=True))
    op.add_column('station', sa.Column('airtime', sa.Integer(), nullable=True))
    op.add_column('station', sa.Column('live', sa.Boolean(), nullable=True, server_default='false'))
    op.add_column('station', sa.Column('callLetters', sa.String(), nullable=True))


def downgrade():
    op.drop_column('station', 'callLetters')
    op.drop_column('station', 'live')
    op.drop_column('station', 'airtime')
    op.drop_column('station', 'location')
    op.drop_column('station', 'frequency')
"""add local flag to station

Revision ID: a1b2c3d4e5f6
Revises: c60829f6e821
Create Date: 2026-07-21 15:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = 'c60829f6e821'
branch_labels = None
depends_on = None


def upgrade():
    # Marks a station as "local" so the frontend can show it under a Local tab.
    op.add_column(
        'station',
        sa.Column('local', sa.Boolean(), nullable=True, server_default='false'),
    )


def downgrade():
    op.drop_column('station', 'local')

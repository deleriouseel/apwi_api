"""create location table

Revision ID: 8b7bbe8f62dd
Revises: 9f2b103e89f5
Create Date: 2022-10-14 14:55:39.460063

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b7bbe8f62dd'
down_revision = '9f2b103e89f5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('location', sa.Column('idLocation', sa.Integer(), nullable=False, primary_key=True, autoincrement=True ), sa.Column('city', sa.String(), nullable=False), sa.Column('state', sa.String(), nullable=False,), sa.Column('country', sa.String(), nullable=False), sa.UniqueConstraint('idLocation'))
    pass


def downgrade() -> None:
    op.drop_table('location')
    pass

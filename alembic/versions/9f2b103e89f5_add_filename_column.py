"""add filename column

Revision ID: 9f2b103e89f5
Revises: 78f1fc77d97f
Create Date: 2022-07-27 14:47:01.607684

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f2b103e89f5'
down_revision = '78f1fc77d97f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('apwi', sa.Column('filename', sa.String(), nullable=True))
    pass 


def downgrade() -> None:
    op.drop_column('apwi', 'filename')
    pass


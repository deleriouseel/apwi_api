"""create network column

Revision ID: dd3e25436e80
Revises: 
Create Date: 2022-06-29 16:41:18.788913

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd3e25436e80'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("apwi", sa.Column("network", sa.String(), nullable=False, server_default="Calvary"))
    pass


def downgrade() -> None:
    op.drop_column("apwi", "network")
    pass

"""remove network default value

Revision ID: f2e6d2f2bb3f
Revises: dd3e25436e80
Create Date: 2022-06-29 16:52:07.086693

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2e6d2f2bb3f'
down_revision = 'dd3e25436e80'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("apwi", "network", server_default=False)
    pass


def downgrade() -> None:
    op.alter_column("apwi", "network", server_default="Calvary")
    pass

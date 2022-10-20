"""add station foreign keys

Revision ID: baa952621d49
Revises: 17ee83bc6bf9
Create Date: 2022-10-20 10:15:58.967758

"""
from tkinter import CASCADE
from alembic import op
import sqlalchemy as sa
from tomlkit import table


# revision identifiers, used by Alembic.
revision = 'baa952621d49'
down_revision = '17ee83bc6bf9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('station', sa.Column('airtime', sa.Integer()))
    op.create_foreign_key('station_airtime_fk', source_table='station', referent_table='airtime', local_cols=['airtime'], remote_cols=['idAirtime'], ondelete='CASCADE')
    op.add_column('station', sa.Column('location', sa.Integer()) )
    op.create_foreign_key('station_location_fk', source_table='station', referent_table='location', local_cols=['location'], remote_cols=['idLocation'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('station_airtime_fk', table_name='station')
    op.drop_column('station', 'airtime')
    op.drop_constraint('station_location_fk', table_name='station')
    op.drop_column('station', 'location')
    pass

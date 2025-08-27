"""create station junction tables

Revision ID: c60829f6e821
Revises: 319454195733
Create Date: 2025-08-27 15:17:31.746984

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c60829f6e821'
down_revision = '319454195733'
branch_labels = None
depends_on = None


def upgrade():
    # Create station_location junction table
    op.create_table(
        'station_location',
        sa.Column('station_id', sa.Integer(), nullable=False),
        sa.Column('location_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['location_id'], ['location.idLocation'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['station_id'], ['station.idStation'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('station_id', 'location_id')
    )

    # Create station_airtime junction table  
    op.create_table(
        'station_airtime',
        sa.Column('station_id', sa.Integer(), nullable=False),
        sa.Column('airtime_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['airtime_id'], ['airtime.idAirtime'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['station_id'], ['station.idStation'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('station_id', 'airtime_id')
    )

def downgrade():
    op.drop_table('station_airtime')
    op.drop_table('station_location')
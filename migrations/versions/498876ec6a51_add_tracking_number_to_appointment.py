"""Add tracking_number to Appointment

Revision ID: 498876ec6a51
Revises: 3f8832827274
Create Date: 2025-06-25 08:09:07.799713
"""
from alembic import op
import sqlalchemy as sa

# Revision identifiers
revision = '498876ec6a51'
down_revision = '3f8832827274'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('appointment', schema=None) as batch_op:
        # Add the new column
        batch_op.add_column(sa.Column('tracking_number', sa.String(length=100), nullable=True))
        # Create a named unique constraint
        batch_op.create_unique_constraint('uq_appointment_tracking_number', ['tracking_number'])
        # Drop the old column (if it exists and is safe to remove)
        batch_op.drop_column('appointment_tracking')

def downgrade():
    with op.batch_alter_table('appointment', schema=None) as batch_op:
        # Add back the old column
        batch_op.add_column(sa.Column('appointment_tracking', sa.String(length=50), nullable=True))
        # Drop the unique constraint on the new column
        batch_op.drop_constraint('uq_appointment_tracking_number', type_='unique')
        # Drop the new column
        batch_op.drop_column('tracking_number')

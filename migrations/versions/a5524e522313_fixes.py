"""Fixes

Revision ID: a5524e522313
Revises: 498876ec6a51
Create Date: 2025-06-25 08:21:25.006541

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a5524e522313'
down_revision = '498876ec6a51'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('feedback', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tracking_number', sa.String(length=100), nullable=True))
        batch_op.create_unique_constraint('uq_feedback_tracking_number', ['tracking_number'])
        batch_op.drop_column('feedback_tracking')

    with op.batch_alter_table('payment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tracking_number', sa.String(length=100), nullable=True))
        batch_op.create_unique_constraint('uq_payment_tracking_number', ['tracking_number'])
        batch_op.drop_column('payment_tracking')

def downgrade():
    with op.batch_alter_table('payment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('payment_tracking', sa.VARCHAR(length=50), nullable=False))
        batch_op.drop_constraint('uq_payment_tracking_number', type_='unique')
        batch_op.create_unique_constraint('uq_tracking_number_payment', ['payment_tracking'])
        batch_op.drop_column('tracking_number')

    with op.batch_alter_table('feedback', schema=None) as batch_op:
        batch_op.add_column(sa.Column('feedback_tracking', sa.VARCHAR(length=50), nullable=False))
        batch_op.drop_constraint('uq_feedback_tracking_number', type_='unique')
        batch_op.create_unique_constraint('uq_tracking_number_feedback', ['feedback_tracking'])
        batch_op.drop_column('tracking_number')

"""add is_enabled_celebrity_new_poll_notif to user

Revision ID: 8f93fedac76f
Revises: cb68250e3497
Create Date: 2017-11-21 16:20:49.698419

"""
import os

from alembic import op
import sqlalchemy as sa

schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = '8f93fedac76f'
down_revision = 'cb68250e3497'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("user", schema=schema_name) as batch_op:
        batch_op.add_column(
            sa.Column('is_enabled_celebrity_new_poll_notif',
                      sa.Boolean, server_default='True'))


def downgrade():
    with op.batch_alter_table("user", schema=schema_name) as batch_op:
        batch_op.drop_column('is_enabled_celebrity_new_poll_notif')

"""change notification setting to default on

Revision ID: c817ad440ab6
Revises: 8f93fedac76f
Create Date: 2017-11-21 16:21:38.281407

"""
import os

from alembic import op
import sqlalchemy as sa

schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = 'c817ad440ab6'
down_revision = '8f93fedac76f'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("user", schema=schema_name) as batch_op:
        batch_op.alter_column(
            'is_enabled_interested_new_poll_notif',
            server_default='True')
        batch_op.alter_column(
            'is_enabled_new_answer_notif',
            server_default='True')


def downgrade():
    with op.batch_alter_table("user", schema=schema_name) as batch_op:
        batch_op.alter_column(
            'is_enabled_interested_new_poll_notif',
            server_default=None)
        batch_op.alter_column(
            'is_enabled_new_answer_notif',
            server_default=None)

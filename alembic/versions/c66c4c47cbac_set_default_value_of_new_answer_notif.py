"""set default value of new answer notif

Revision ID: c66c4c47cbac
Revises: c817ad440ab6
Create Date: 2017-11-29 15:39:02.412490

"""
import os

from alembic import op
import sqlalchemy as sa

schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = 'c66c4c47cbac'
down_revision = 'c817ad440ab6'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("user", schema=schema_name) as batch_op:
        batch_op.alter_column('is_enabled_new_answer_notif', server_default='False')


def downgrade():
    with op.batch_alter_table("user", schema=schema_name) as batch_op:
        batch_op.alter_column('is_enabled_new_answer_notif', server_default='True')

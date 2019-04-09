"""add notification settings to user

Revision ID: 654eebb248a8
Revises: ee280b6785d0
Create Date: 2017-10-09 17:11:17.684252

"""
import os

from alembic import op
import sqlalchemy as sa


schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = '654eebb248a8'
down_revision = 'ee280b6785d0'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("user", schema=schema_name) as batch_op:
        batch_op.add_column(
            sa.Column('is_enabled_interested_new_poll_notif', sa.Boolean, server_default='False'))
        batch_op.add_column(
            sa.Column('is_enabled_new_answer_notif', sa.Boolean, server_default='False'))


def downgrade():
    with op.batch_alter_table("user", schema=schema_name) as batch_op:
        batch_op.drop_column('is_enabled_interested_new_poll_notif')
        batch_op.drop_column('is_enabled_new_answer_notif')

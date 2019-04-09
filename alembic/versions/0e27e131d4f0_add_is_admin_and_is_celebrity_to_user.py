"""add is admin and is celebrity to user

Revision ID: 0e27e131d4f0
Revises: 7ac314ee29f3
Create Date: 2017-10-26 15:06:53.025334

"""
import os

from alembic import op
import sqlalchemy as sa


schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = '0e27e131d4f0'
down_revision = '7ac314ee29f3'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("user", schema=schema_name) as batch_op:
        batch_op.add_column(
            sa.Column('is_admin', sa.Boolean, server_default='False'))
        batch_op.add_column(
            sa.Column('is_celebrity', sa.Boolean, server_default='False'))


def downgrade():
    with op.batch_alter_table("user", schema=schema_name) as batch_op:
        batch_op.drop_column('is_admin')
        batch_op.drop_column('is_celebrity')

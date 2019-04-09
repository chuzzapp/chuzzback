"""add is_linked_to_instagram to user

Revision ID: cb68250e3497
Revises: a0e1e4835720
Create Date: 2017-11-17 19:49:08.234509

"""
import os

from alembic import op
import sqlalchemy as sa

schema_name = os.getenv('SCHEMA_NAME')

# revision identifiers, used by Alembic.
revision = 'cb68250e3497'
down_revision = 'a0e1e4835720'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("user", schema=schema_name) as batch_op:
        batch_op.add_column(
            sa.Column('is_linked_to_instagram', sa.Boolean, server_default='False'))


def downgrade():
    with op.batch_alter_table("user", schema=schema_name) as batch_op:
        batch_op.drop_column('is_linked_to_instagram')

"""add deleted to user

Revision ID: a75c99aabe00
Revises: c66c4c47cbac
Create Date: 2017-11-30 14:54:26.690396

"""
import os

from alembic import op
import sqlalchemy as sa


schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = 'a75c99aabe00'
down_revision = 'c66c4c47cbac'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("user", schema=schema_name) as batch_op:
        batch_op.add_column(
            sa.Column('deleted', sa.Boolean, server_default='False'))


def downgrade():
    with op.batch_alter_table("user", schema=schema_name) as batch_op:
        batch_op.drop_column('deleted')

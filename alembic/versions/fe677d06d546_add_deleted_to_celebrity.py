"""add deleted to celebrity

Revision ID: fe677d06d546
Revises: a75c99aabe00
Create Date: 2017-11-30 16:36:36.552459

"""
import os

from alembic import op
import sqlalchemy as sa


schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = 'fe677d06d546'
down_revision = 'a75c99aabe00'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("celebrity", schema=schema_name) as batch_op:
        batch_op.add_column(
            sa.Column('deleted', sa.Boolean, server_default='False'))


def downgrade():
    with op.batch_alter_table("celebrity", schema=schema_name) as batch_op:
        batch_op.drop_column('deleted')

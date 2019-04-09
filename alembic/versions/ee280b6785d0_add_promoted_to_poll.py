"""add promoted to poll

Revision ID: ee280b6785d0
Revises: a216ab491056
Create Date: 2017-10-09 16:52:02.130652

"""
import os

from alembic import op
import sqlalchemy as sa


schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = 'ee280b6785d0'
down_revision = 'a216ab491056'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("poll", schema=schema_name) as batch_op:
        batch_op.add_column(
            sa.Column('promoted', sa.Boolean, server_default='False'))


def downgrade():
    with op.batch_alter_table("poll", schema=schema_name) as batch_op:
        batch_op.drop_column('promoted')

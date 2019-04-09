"""add deleted to question and choice

Revision ID: 6c60ebf42695
Revises: 0717a96ab5fe
Create Date: 2017-10-13 16:47:47.082093

"""
import os

from alembic import op
import sqlalchemy as sa


schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = '6c60ebf42695'
down_revision = '0717a96ab5fe'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("question", schema=schema_name) as batch_op:
        batch_op.add_column(
            sa.Column('deleted', sa.Boolean, server_default='False'))
    with op.batch_alter_table("choice", schema=schema_name) as batch_op:
        batch_op.add_column(
            sa.Column('deleted', sa.Boolean, server_default='False'))


def downgrade():
    with op.batch_alter_table("question", schema=schema_name) as batch_op:
        batch_op.drop_column('deleted')
    with op.batch_alter_table("choice", schema=schema_name) as batch_op:
        batch_op.drop_column('deleted')

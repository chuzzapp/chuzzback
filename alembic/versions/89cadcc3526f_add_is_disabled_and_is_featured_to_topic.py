"""add is_disabled and is_featured to topic

Revision ID: 89cadcc3526f
Revises: 6997f2139ce4
Create Date: 2018-01-19 15:02:53.752885

"""
import os

from alembic import op
import sqlalchemy as sa


schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = '89cadcc3526f'
down_revision = '6997f2139ce4'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("topic", schema=schema_name) as batch_op:
        batch_op.add_column(
            sa.Column('is_disabled', sa.Boolean, server_default='False'))
        batch_op.add_column(
            sa.Column('is_featured', sa.Boolean, server_default='False'))


def downgrade():
    with op.batch_alter_table("topic", schema=schema_name) as batch_op:
        batch_op.drop_column('is_disabled')
        batch_op.drop_column('is_featured')

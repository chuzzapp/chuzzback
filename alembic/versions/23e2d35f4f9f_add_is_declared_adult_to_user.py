"""add is_declared_adult to user

Revision ID: 23e2d35f4f9f
Revises: 5761f8207fad
Create Date: 2018-04-23 17:43:35.011112

"""
import os

from alembic import op
import sqlalchemy as sa

schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = '23e2d35f4f9f'
down_revision = '5761f8207fad'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("user", schema=schema_name) as batch_op:
        batch_op.add_column(
            sa.Column('is_declared_adult', sa.Boolean, server_default='False'))


def downgrade():
    with op.batch_alter_table("user", schema=schema_name) as batch_op:
        batch_op.drop_column('is_declared_adult')

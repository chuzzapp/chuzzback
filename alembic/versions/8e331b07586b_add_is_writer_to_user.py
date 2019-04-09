"""add is_writer to user

Revision ID: 8e331b07586b
Revises: 23e2d35f4f9f
Create Date: 2018-04-24 14:30:03.785805

"""
import os

from alembic import op
import sqlalchemy as sa

schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = '8e331b07586b'
down_revision = '23e2d35f4f9f'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("user", schema=schema_name) as batch_op:
        batch_op.add_column(
            sa.Column('is_writer', sa.Boolean, server_default='False'))


def downgrade():
    with op.batch_alter_table("user", schema=schema_name) as batch_op:
        batch_op.drop_column('is_writer')

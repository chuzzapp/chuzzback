"""add is_published to poll

Revision ID: 642b0bdd7db3
Revises: 8e331b07586b
Create Date: 2018-04-24 14:36:19.213006

"""
import os

from alembic import op
import sqlalchemy as sa

schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = '642b0bdd7db3'
down_revision = '8e331b07586b'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("poll", schema=schema_name) as batch_op:
        batch_op.add_column(
            sa.Column('is_published', sa.Boolean, server_default='True'))


def downgrade():
    with op.batch_alter_table("poll", schema=schema_name) as batch_op:
        batch_op.drop_column('is_published')

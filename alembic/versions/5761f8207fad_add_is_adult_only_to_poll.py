"""add is_adult_only to poll

Revision ID: 5761f8207fad
Revises: 493b84715c67
Create Date: 2018-04-23 17:40:59.945705

"""
import os

from alembic import op
import sqlalchemy as sa

schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = '5761f8207fad'
down_revision = '493b84715c67'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("poll", schema=schema_name) as batch_op:
        batch_op.add_column(
            sa.Column('is_adult_only', sa.Boolean, server_default='False'))


def downgrade():
    with op.batch_alter_table("poll", schema=schema_name) as batch_op:
        batch_op.drop_column('is_adult_only')

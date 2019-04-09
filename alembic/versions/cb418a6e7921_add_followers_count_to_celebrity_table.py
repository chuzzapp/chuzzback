"""add followers_count to celebrity table

Revision ID: cb418a6e7921
Revises: 86eddbb29a39
Create Date: 2017-11-06 12:00:09.100233

"""
import os
from alembic import op
import sqlalchemy as sa

schema_name = os.getenv('SCHEMA_NAME')

# revision identifiers, used by Alembic.
revision = 'cb418a6e7921'
down_revision = '86eddbb29a39'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("celebrity", schema=schema_name) as batch_op:
        batch_op.add_column(
            sa.Column('followers_count', sa.Integer))


def downgrade():
    with op.batch_alter_table("celebrity", schema=schema_name) as batch_op:
        batch_op.drop_column('followers_count')

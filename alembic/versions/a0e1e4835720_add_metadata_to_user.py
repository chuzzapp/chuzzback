"""add metadata to user

Revision ID: a0e1e4835720
Revises: e2b742369866
Create Date: 2017-11-16 10:31:41.178678

"""
import os

from alembic import op
import sqlalchemy as sa

schema_name = os.getenv('SCHEMA_NAME')

# revision identifiers, used by Alembic.
revision = 'a0e1e4835720'
down_revision = 'e2b742369866'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user', schema=schema_name) as batch_op:
        batch_op.add_column(
            sa.Column('metadata', sa.dialects.postgresql.JSONB))


def downgrade():
    with op.batch_alter_table('user', schema=schema_name) as batch_op:
        batch_op.drop_column('metadata')

"""add display name to celebrity

Revision ID: 42abd09b5c3b
Revises: a7c056e10dd8
Create Date: 2017-10-09 15:21:38.225017

"""
import os

from alembic import op
import sqlalchemy as sa


schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = '42abd09b5c3b'
down_revision = 'a7c056e10dd8'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("celebrity", schema=schema_name) as batch_op:
        batch_op.add_column(
            sa.Column('display_name', sa.Text, nullable=False))
        batch_op.drop_column('first_name')
        batch_op.drop_column('last_name')


def downgrade():
    with op.batch_alter_table("celebrity", schema=schema_name) as batch_op:
        batch_op.add_column(
            sa.Column('first_name', sa.Text))
        batch_op.add_column(
            sa.Column('last_name', sa.Text))
        batch_op.drop_column('display_name')

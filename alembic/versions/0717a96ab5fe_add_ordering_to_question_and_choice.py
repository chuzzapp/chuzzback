"""add ordering to question and choice

Revision ID: 0717a96ab5fe
Revises: c1b4f16930df
Create Date: 2017-10-13 12:02:29.295628

"""
import os

from alembic import op
import sqlalchemy as sa


schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = '0717a96ab5fe'
down_revision = 'c1b4f16930df'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("question", schema=schema_name) as batch_op:
        batch_op.add_column(
            sa.Column('ordering', sa.Integer, nullable=False))
    with op.batch_alter_table("choice", schema=schema_name) as batch_op:
        batch_op.add_column(
            sa.Column('ordering', sa.Integer, nullable=False))


def downgrade():
    with op.batch_alter_table("question", schema=schema_name) as batch_op:
        batch_op.drop_column('ordering')
    with op.batch_alter_table("choice", schema=schema_name) as batch_op:
        batch_op.drop_column('ordering')

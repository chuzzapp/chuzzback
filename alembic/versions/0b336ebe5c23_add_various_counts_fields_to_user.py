"""add various counts fields to user

Revision ID: 0b336ebe5c23
Revises: 0e27e131d4f0
Create Date: 2017-10-30 16:45:03.486403

"""
import os

from alembic import op
import sqlalchemy as sa

schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = '0b336ebe5c23'
down_revision = '0e27e131d4f0'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("user", schema=schema_name) as batch_op:
        batch_op.add_column(
            sa.Column('answers_count', sa.Integer))
        batch_op.add_column(
            sa.Column('groups_count', sa.Integer))
        batch_op.add_column(
            sa.Column('likes_count', sa.Integer))
        batch_op.add_column(
            sa.Column('polls_count', sa.Integer))
        batch_op.add_column(
            sa.Column('followers_count', sa.Integer))
        batch_op.add_column(
            sa.Column('following_count', sa.Integer))


def downgrade():
    with op.batch_alter_table("user", schema=schema_name) as batch_op:
        batch_op.drop_column('answers_count')
        batch_op.drop_column('groups_count')
        batch_op.drop_column('likes_count')
        batch_op.drop_column('polls_count')
        batch_op.drop_column('followers_count')
        batch_op.drop_column('following_count')

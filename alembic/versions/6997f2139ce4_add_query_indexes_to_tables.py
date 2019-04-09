"""add query indexes to tables

Revision ID: 6997f2139ce4
Revises: f1d362074b71
Create Date: 2017-12-21 14:32:09.922263

"""
import os

from alembic import op
import sqlalchemy as sa

schema_name = os.getenv('SCHEMA_NAME')

# revision identifiers, used by Alembic.
revision = '6997f2139ce4'
down_revision = 'f1d362074b71'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index('celebrity_user_id_index', 'celebrity', ['user_id'], schema=schema_name)
    op.create_index('user_country_id_index', 'user', ['country_id'], schema=schema_name)
    op.create_index('poll_country_id_index', 'poll', ['country_id'], schema=schema_name)
    op.create_index('poll_user_id_index', 'poll', ['user_id'], schema=schema_name)
    op.create_index('question_poll_id_index', 'question', ['poll_id'], schema=schema_name)


def downgrade():
    op.drop_index('celebrity_user_id_index', schema=schema_name)
    op.drop_index('user_country_id_index', schema=schema_name)
    op.drop_index('poll_country_id_index', schema=schema_name)
    op.drop_index('poll_user_id_index', schema=schema_name)
    op.drop_index('question_poll_id_index', schema=schema_name)

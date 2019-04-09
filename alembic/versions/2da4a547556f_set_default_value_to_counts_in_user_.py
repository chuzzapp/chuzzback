"""set default value to counts in user and celebrity

Revision ID: 2da4a547556f
Revises: b87a5228ede5
Create Date: 2017-11-13 09:47:05.439675

"""
import os

from alembic import op
import sqlalchemy as sa

schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = '2da4a547556f'
down_revision = 'b87a5228ede5'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("user", schema=schema_name) as batch_op:
        batch_op.alter_column('answers_count', server_default='0')
        batch_op.alter_column('groups_count', server_default='0')
        batch_op.alter_column('likes_count', server_default='0')
        batch_op.alter_column('polls_count', server_default='0')
        batch_op.alter_column('followers_count', server_default='0')
        batch_op.alter_column('following_count', server_default='0')

    with op.batch_alter_table("celebrity", schema=schema_name) as batch_op:
        batch_op.alter_column('followers_count', server_default='0')


def downgrade():
    with op.batch_alter_table("user", schema=schema_name) as batch_op:
        batch_op.alter_column('answers_count', server_default=None)
        batch_op.alter_column('groups_count', server_default=None)
        batch_op.alter_column('likes_count', server_default=None)
        batch_op.alter_column('polls_count', server_default=None)
        batch_op.alter_column('followers_count', server_default=None)
        batch_op.alter_column('following_count', server_default=None)

    with op.batch_alter_table("celebrity", schema=schema_name) as batch_op:
        batch_op.alter_column('followers_count', server_default=None)

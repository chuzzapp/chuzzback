"""remove sexual preference and selected topics from user

Revision ID: 239ed15d4c2c
Revises: a2016e420b2f
Create Date: 2017-10-09 14:57:24.803106

"""
import os

from alembic import op
import sqlalchemy as sa


schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = '239ed15d4c2c'
down_revision = 'a2016e420b2f'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("user", schema=schema_name) as batch_op:
        batch_op.drop_column('sexual_preference')
        batch_op.drop_column('selected_topics')


def downgrade():
    with op.batch_alter_table("user", schema=schema_name) as batch_op:
        batch_op.add_column(
            sa.Column('sexual_preference', sa.Text))
        batch_op.add_column(
            sa.Column('selected_topics', sa.dialects.postgresql.JSONB))
    op.create_check_constraint("constraint_check_sexual_preference", "user", "sexual_preference = ANY(ARRAY['heterosexual', 'homosexual', 'bisexual'])", schema=schema_name)

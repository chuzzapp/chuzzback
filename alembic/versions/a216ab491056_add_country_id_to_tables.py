"""add country id to tables

Revision ID: a216ab491056
Revises: 313c8337d388
Create Date: 2017-10-09 16:05:44.660611

"""
import os

from alembic import op
import sqlalchemy as sa


schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = 'a216ab491056'
down_revision = '313c8337d388'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("user", schema=schema_name) as batch_op:
        batch_op.drop_column('country')
        batch_op.add_column(
            sa.Column('country_id', sa.Text))
    op.create_foreign_key(
        'user_country__id', 'user', 'country',
        ['country_id'], ['_id'], source_schema='%s' % schema_name, referent_schema='%s' % schema_name)
    with op.batch_alter_table("poll", schema=schema_name) as batch_op:
        batch_op.add_column(
            sa.Column('country_id', sa.Text))
    op.create_foreign_key(
        'poll_country__id', 'poll', 'country',
        ['country_id'], ['_id'], source_schema='%s' % schema_name, referent_schema='%s' % schema_name)
    with op.batch_alter_table("celebrity", schema=schema_name) as batch_op:
        batch_op.add_column(
            sa.Column('country_id', sa.Text))
    op.create_foreign_key(
        'celebrity_country__id', 'celebrity', 'country',
        ['country_id'], ['_id'], source_schema='%s' % schema_name, referent_schema='%s' % schema_name)


def downgrade():
    op.drop_constraint('user_country__id', 'user', schema='%s' % schema_name)
    with op.batch_alter_table("user", schema=schema_name) as batch_op:
        batch_op.add_column(
            sa.Column('country', sa.Text, nullable=False))
        batch_op.drop_column('country_id')
    op.drop_constraint('poll_country__id', 'poll', schema='%s' % schema_name)
    with op.batch_alter_table("poll", schema=schema_name) as batch_op:
        batch_op.drop_column('country_id')
    op.drop_constraint('celebrity_country__id', 'celebrity', schema='%s' % schema_name)
    with op.batch_alter_table("celebrity", schema=schema_name) as batch_op:
        batch_op.drop_column('country_id')

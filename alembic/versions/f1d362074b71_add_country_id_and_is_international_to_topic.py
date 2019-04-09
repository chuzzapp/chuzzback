"""add country id and is international to topic

Revision ID: f1d362074b71
Revises: fe677d06d546
Create Date: 2017-12-07 15:26:09.488600

"""
import os

from alembic import op
import sqlalchemy as sa


schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = 'f1d362074b71'
down_revision = 'fe677d06d546'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("topic", schema=schema_name) as batch_op:
        batch_op.add_column(
            sa.Column('country_id', sa.Text))
        batch_op.add_column(
            sa.Column('is_international', sa.Boolean, server_default='False'))
    op.create_foreign_key(
        'user_country__id', 'topic', 'country',
        ['country_id'], ['_id'], source_schema='%s' % schema_name, referent_schema='%s' % schema_name)


def downgrade():
    op.drop_constraint('user_country__id', 'topic', schema='%s' % schema_name)
    with op.batch_alter_table("topic", schema=schema_name) as batch_op:
        batch_op.drop_column('country_id')
        batch_op.drop_column('is_international')

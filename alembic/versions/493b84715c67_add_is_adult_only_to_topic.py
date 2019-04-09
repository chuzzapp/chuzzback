"""add is_adult_only to topic

Revision ID: 493b84715c67
Revises: b4364f33391d
Create Date: 2018-04-23 17:38:12.708166

"""
import os

from alembic import op
import sqlalchemy as sa

schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = '493b84715c67'
down_revision = 'b4364f33391d'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("topic", schema=schema_name) as batch_op:
        batch_op.add_column(
            sa.Column('is_adult_only', sa.Boolean, server_default='False'))


def downgrade():
    with op.batch_alter_table("topic", schema=schema_name) as batch_op:
        batch_op.drop_column('is_adult_only')

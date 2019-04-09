"""add first name and last name to user

Revision ID: a2016e420b2f
Revises: 20640e29e224
Create Date: 2017-10-09 14:53:24.857726

"""
import os

from alembic import op
import sqlalchemy as sa


schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = 'a2016e420b2f'
down_revision = '20640e29e224'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("user", schema=schema_name) as batch_op:
        batch_op.add_column(
            sa.Column('first_name', sa.Text))
        batch_op.add_column(
            sa.Column('last_name', sa.Text))


def downgrade():
    with op.batch_alter_table("user", schema=schema_name) as batch_op:
        batch_op.drop_column('first_name')
        batch_op.drop_column('last_name')

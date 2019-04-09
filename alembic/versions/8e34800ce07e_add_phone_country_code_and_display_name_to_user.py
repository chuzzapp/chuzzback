"""add phone country code and display name to user

Revision ID: 8e34800ce07e
Revises: 42abd09b5c3b
Create Date: 2017-10-09 15:45:33.853814

"""
import os

from alembic import op
import sqlalchemy as sa


schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = '8e34800ce07e'
down_revision = '42abd09b5c3b'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("user", schema=schema_name) as batch_op:
        batch_op.add_column(
            sa.Column('phone_country_code', sa.Text))
        batch_op.add_column(
            sa.Column('display_name', sa.Text))


def downgrade():
    with op.batch_alter_table("user", schema=schema_name) as batch_op:
        batch_op.drop_column('phone_country_code')
        batch_op.drop_column('display_name')

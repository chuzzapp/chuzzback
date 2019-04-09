"""add is first_answer_count to user

Revision ID: 22f4b2dd032f
Revises: 14e051eddca5
Create Date: 2018-07-25 09:17:22.713349

"""
import os
from alembic import op
import sqlalchemy as sa

schema_name = os.getenv('SCHEMA_NAME')

# revision identifiers, used by Alembic.
revision = '22f4b2dd032f'
down_revision = '14e051eddca5'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("user", schema=schema_name) as batch_op:
        batch_op.add_column(
            sa.Column('first_answer_count', sa.Integer,server_default='0'))


def downgrade():
    with op.batch_alter_table("user", schema=schema_name) as batch_op:
        batch_op.drop_column('first_answer_count')

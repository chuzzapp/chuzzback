"""remove not null from poll description

Revision ID: 9392809b1fe6
Revises: 89cadcc3526f
Create Date: 2018-01-22 16:43:19.862803

"""
import os

from alembic import op
import sqlalchemy as sa


schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = '9392809b1fe6'
down_revision = '89cadcc3526f'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("poll", schema=schema_name) as batch_op:
        batch_op.alter_column('description', nullable=True)


def downgrade():
    with op.batch_alter_table("poll", schema=schema_name) as batch_op:
        batch_op.alter_column('description', nullable=False)

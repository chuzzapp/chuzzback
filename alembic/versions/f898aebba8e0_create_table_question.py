"""create table question

Revision ID: f898aebba8e0
Revises: ef25b2d8f95f
Create Date: 2017-10-04 15:14:19.316457

"""

import os

from alembic import op
import sqlalchemy as sa


schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = 'f898aebba8e0'
down_revision = 'ef25b2d8f95f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'question',
        sa.Column('_id', sa.Text, nullable=False, unique=True),
        sa.Column('_database_id', sa.Text, nullable=False),
        sa.Column('_owner_id', sa.Text, nullable=False),
        sa.Column('_access', sa.dialects.postgresql.JSONB),
        sa.Column('_created_by', sa.Text),
        sa.Column('_created_at', sa.DateTime, nullable=False),
        sa.Column('_updated_by', sa.Text),
        sa.Column('_updated_at', sa.DateTime, nullable=False),
        sa.Column('title', sa.Text, nullable=False),
        sa.Column('type', sa.Text, nullable=False),
        sa.Column('poll_id', sa.Text, nullable=False),
        sa.PrimaryKeyConstraint('_id', '_database_id', '_owner_id'),
        sa.ForeignKeyConstraint(['poll_id'], ['%s.poll._id' % schema_name]),
        schema=schema_name
    )

    op.execute(
    """
    CREATE TRIGGER trigger_notify_record_change
    AFTER INSERT OR UPDATE OR DELETE
    ON %s.question
    FOR EACH ROW
    EXECUTE PROCEDURE public.notify_record_change();
    """ % schema_name
    )


def downgrade():
    op.drop_table('question', schema=schema_name)

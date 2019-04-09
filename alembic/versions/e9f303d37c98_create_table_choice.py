"""create table choice

Revision ID: e9f303d37c98
Revises: f898aebba8e0
Create Date: 2017-10-04 15:41:38.200255

"""
import os

from alembic import op
import sqlalchemy as sa


schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = 'e9f303d37c98'
down_revision = 'f898aebba8e0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'choice',
        sa.Column('_id', sa.Text, nullable=False, unique=True),
        sa.Column('_database_id', sa.Text, nullable=False),
        sa.Column('_owner_id', sa.Text, nullable=False),
        sa.Column('_access', sa.dialects.postgresql.JSONB),
        sa.Column('_created_by', sa.Text),
        sa.Column('_created_at', sa.DateTime, nullable=False),
        sa.Column('_updated_by', sa.Text),
        sa.Column('_updated_at', sa.DateTime, nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('question_id', sa.Text, nullable=False),
        sa.Column('image_id', sa.Text),
        sa.Column('select_count', sa.Integer, server_default='0'),
        sa.PrimaryKeyConstraint('_id', '_database_id', '_owner_id'),
        sa.ForeignKeyConstraint(['question_id'], ['%s.question._id' % schema_name]),
        sa.ForeignKeyConstraint(['image_id'], ['%s._asset.id' % schema_name]),
        schema=schema_name
    )

    op.execute(
    """
    CREATE TRIGGER trigger_notify_record_change
    AFTER INSERT OR UPDATE OR DELETE
    ON %s.choice
    FOR EACH ROW
    EXECUTE PROCEDURE public.notify_record_change();
    """ % schema_name
    )


def downgrade():
    op.drop_table('choice', schema=schema_name)

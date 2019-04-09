"""create table user topic

Revision ID: a7c056e10dd8
Revises: 239ed15d4c2c
Create Date: 2017-10-09 15:12:46.431026

"""
import os

from alembic import op
import sqlalchemy as sa


schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = 'a7c056e10dd8'
down_revision = '239ed15d4c2c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user_topic',
        sa.Column('_id', sa.Text, nullable=False, unique=True),
        sa.Column('_database_id', sa.Text, nullable=False),
        sa.Column('_owner_id', sa.Text, nullable=False),
        sa.Column('_access', sa.dialects.postgresql.JSONB),
        sa.Column('_created_by', sa.Text, nullable=False),
        sa.Column('_created_at', sa.DateTime),
        sa.Column('_updated_by', sa.Text, nullable=False),
        sa.Column('_updated_at', sa.DateTime),
        sa.Column('user_id', sa.Text, nullable=False),
        sa.Column('topic_id', sa.Text, nullable=False),
        sa.PrimaryKeyConstraint('_id', '_database_id', '_owner_id'),
        sa.UniqueConstraint('user_id', 'topic_id'),
        sa.ForeignKeyConstraint(['user_id'], ['%s.user._id' % schema_name]),
        sa.ForeignKeyConstraint(['topic_id'], ['%s.topic._id' % schema_name]),
        schema=schema_name
    )

    op.execute(
    """
    CREATE TRIGGER trigger_notify_record_change
    AFTER INSERT OR UPDATE OR DELETE
    ON %s.user_topic
    FOR EACH ROW
    EXECUTE PROCEDURE public.notify_record_change();
    """ % schema_name
    )


def downgrade():
    op.drop_table('user_topic', schema=schema_name)

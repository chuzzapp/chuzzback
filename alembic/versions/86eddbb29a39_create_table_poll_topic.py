"""create table poll topic

Revision ID: 86eddbb29a39
Revises: 0b336ebe5c23
Create Date: 2017-11-02 16:42:28.999485

"""
import os

from alembic import op
import sqlalchemy as sa


schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = '86eddbb29a39'
down_revision = '0b336ebe5c23'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'poll_topic',
        sa.Column('_id', sa.Text, nullable=False, unique=True),
        sa.Column('_database_id', sa.Text, nullable=False),
        sa.Column('_owner_id', sa.Text, nullable=False),
        sa.Column('_access', sa.dialects.postgresql.JSONB),
        sa.Column('_created_by', sa.Text, nullable=False),
        sa.Column('_created_at', sa.DateTime),
        sa.Column('_updated_by', sa.Text, nullable=False),
        sa.Column('_updated_at', sa.DateTime),
        sa.Column('poll_id', sa.Text, nullable=False),
        sa.Column('topic_id', sa.Text, nullable=False),
        sa.PrimaryKeyConstraint('_id', '_database_id', '_owner_id'),
        sa.UniqueConstraint('poll_id', 'topic_id'),
        sa.ForeignKeyConstraint(['poll_id'], ['%s.poll._id' % schema_name]),
        sa.ForeignKeyConstraint(['topic_id'], ['%s.topic._id' % schema_name]),
        schema=schema_name
    )

    op.execute(
    """
    CREATE TRIGGER trigger_notify_record_change
    AFTER INSERT OR UPDATE OR DELETE
    ON %s.poll_topic
    FOR EACH ROW
    EXECUTE PROCEDURE public.notify_record_change();
    """ % schema_name
    )

    op.drop_constraint('poll_topic_id_fkey', 'poll', schema='%s' % schema_name)

    with op.batch_alter_table("poll", schema=schema_name) as batch_op:
        batch_op.drop_column('topic_id')


def downgrade():
    op.drop_table('poll_topic', schema=schema_name)
    with op.batch_alter_table("poll", schema=schema_name) as batch_op:
        batch_op.add_column(
            sa.Column('topic_id', sa.Text))

    op.create_foreign_key(
        'poll_topic_id_fkey', 'poll', 'topic',
        ['topic_id'], ['_id'], source_schema='%s' % schema_name, referent_schema='%s' % schema_name)

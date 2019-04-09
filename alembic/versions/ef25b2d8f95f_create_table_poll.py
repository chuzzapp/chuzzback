"""create table poll

Revision ID: ef25b2d8f95f
Revises: f22342161853
Create Date: 2017-10-04 14:41:26.486289

"""
import os

from alembic import op
import sqlalchemy as sa


schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = 'ef25b2d8f95f'
down_revision = 'f22342161853'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'poll',
        sa.Column('_id', sa.Text, nullable=False, unique=True),
        sa.Column('_database_id', sa.Text, nullable=False),
        sa.Column('_owner_id', sa.Text, nullable=False),
        sa.Column('_access', sa.dialects.postgresql.JSONB),
        sa.Column('_created_by', sa.Text),
        sa.Column('_created_at', sa.DateTime, nullable=False),
        sa.Column('_updated_by', sa.Text),
        sa.Column('_updated_at', sa.DateTime, nullable=False),
        sa.Column('name', sa.Text, nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('user_id', sa.Text),
        sa.Column('start_time', sa.DateTime, nullable=False),
        sa.Column('end_time', sa.DateTime, nullable=False),
        sa.Column('topic_id', sa.Text),
        sa.Column('image_id', sa.Text),
        sa.Column('is_active', sa.Boolean),
        sa.Column('is_live', sa.Boolean, server_default='False'),
        sa.Column('likes', sa.Integer, server_default='0'),
        sa.Column('answers', sa.Integer, server_default='0'),
        sa.Column('views', sa.Integer, server_default='0'),
        sa.PrimaryKeyConstraint('_id', '_database_id', '_owner_id'),
        sa.ForeignKeyConstraint(['user_id'], ['%s.user._id' % schema_name]),
        sa.ForeignKeyConstraint(['topic_id'], ['%s.topic._id' % schema_name]),
        sa.ForeignKeyConstraint(['image_id'], ['%s._asset.id' % schema_name]),
        schema=schema_name
    )

    op.execute(
    """
    CREATE TRIGGER trigger_notify_record_change
    AFTER INSERT OR UPDATE OR DELETE
    ON %s.poll
    FOR EACH ROW
    EXECUTE PROCEDURE public.notify_record_change();
    """ % schema_name
    )


def downgrade():
    op.drop_table('poll', schema=schema_name)

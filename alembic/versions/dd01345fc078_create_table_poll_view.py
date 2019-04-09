"""create table poll view

Revision ID: dd01345fc078
Revises: ddedd046aa69
Create Date: 2017-10-04 16:58:40.065857

"""
import os

from alembic import op
import sqlalchemy as sa


schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = 'dd01345fc078'
down_revision = 'ddedd046aa69'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'poll_view',
        sa.Column('_id', sa.Text, nullable=False, unique=True),
        sa.Column('_database_id', sa.Text, nullable=False),
        sa.Column('_owner_id', sa.Text, nullable=False),
        sa.Column('_access', sa.dialects.postgresql.JSONB),
        sa.Column('_created_by', sa.Text),
        sa.Column('_created_at', sa.DateTime, nullable=False),
        sa.Column('_updated_by', sa.Text),
        sa.Column('_updated_at', sa.DateTime, nullable=False),
        sa.Column('user_id', sa.Text, nullable=False),
        sa.Column('poll_id', sa.Text, nullable=False),
        sa.PrimaryKeyConstraint('_id', '_database_id', '_owner_id'),
        sa.UniqueConstraint('user_id', 'poll_id'),
        sa.ForeignKeyConstraint(['user_id'], ['%s.user._id' % schema_name]),
        sa.ForeignKeyConstraint(['poll_id'], ['%s.poll._id' % schema_name]),
        schema=schema_name
    )

    op.execute(
    """
    CREATE TRIGGER trigger_notify_record_change
    AFTER INSERT OR UPDATE OR DELETE
    ON %s.poll_view
    FOR EACH ROW
    EXECUTE PROCEDURE public.notify_record_change();
    """ % schema_name
    )


def downgrade():
    op.drop_table('poll_view', schema=schema_name)

"""create table celebrity

Revision ID: 7f2faebd2013
Revises: dd01345fc078
Create Date: 2017-10-04 17:03:44.800030

"""
import os

from alembic import op
import sqlalchemy as sa


schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = '7f2faebd2013'
down_revision = 'dd01345fc078'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'celebrity',
        sa.Column('_id', sa.Text, nullable=False, unique=True),
        sa.Column('_database_id', sa.Text, nullable=False),
        sa.Column('_owner_id', sa.Text, nullable=False),
        sa.Column('_access', sa.dialects.postgresql.JSONB),
        sa.Column('_created_by', sa.Text),
        sa.Column('_created_at', sa.DateTime, nullable=False),
        sa.Column('_updated_by', sa.Text),
        sa.Column('_updated_at', sa.DateTime, nullable=False),
        sa.Column('username', sa.Text),
        sa.Column('first_name', sa.Text),
        sa.Column('last_name', sa.Text),
        sa.Column('image_id', sa.Text),
        sa.Column('user_id', sa.Text),
        sa.UniqueConstraint('username'),
        sa.PrimaryKeyConstraint('_id', '_database_id', '_owner_id'),
        sa.ForeignKeyConstraint(['user_id'], ['%s.user._id' % schema_name]),
        sa.ForeignKeyConstraint(['image_id'], ['%s._asset.id' % schema_name]),
        schema=schema_name
    )

    op.execute(
    """
    CREATE TRIGGER trigger_notify_record_change
    AFTER INSERT OR UPDATE OR DELETE
    ON %s.celebrity
    FOR EACH ROW
    EXECUTE PROCEDURE public.notify_record_change();
    """ % schema_name
    )


def downgrade():
    op.drop_table('celebrity', schema=schema_name)

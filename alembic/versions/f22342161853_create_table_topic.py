"""create table topic

Revision ID: f22342161853
Revises: a3315cf6595d
Create Date: 2017-10-04 14:20:49.948136

"""
import os

from alembic import op
import sqlalchemy as sa


schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = 'f22342161853'
down_revision = 'a3315cf6595d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'topic',
        sa.Column('_id', sa.Text, nullable=False, unique=True),
        sa.Column('_database_id', sa.Text, nullable=False),
        sa.Column('_owner_id', sa.Text, nullable=False),
        sa.Column('_access', sa.dialects.postgresql.JSONB),
        sa.Column('_created_by', sa.Text),
        sa.Column('_created_at', sa.DateTime, nullable=False),
        sa.Column('_updated_by', sa.Text),
        sa.Column('_updated_at', sa.DateTime, nullable=False),
        sa.Column('name', sa.Text, nullable=False),
        sa.Column('image_id', sa.Text),
        sa.PrimaryKeyConstraint('_id', '_database_id', '_owner_id'),
        sa.ForeignKeyConstraint(['image_id'], ['%s._asset.id' % schema_name]),
        schema=schema_name
    )

    op.execute(
    """
    CREATE TRIGGER trigger_notify_record_change
    AFTER INSERT OR UPDATE OR DELETE
    ON %s.topic
    FOR EACH ROW
    EXECUTE PROCEDURE public.notify_record_change();
    """ % schema_name
    )


def downgrade():
    op.drop_table('topic', schema=schema_name)

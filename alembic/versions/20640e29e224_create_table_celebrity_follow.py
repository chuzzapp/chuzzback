"""create table celebrity follow

Revision ID: 20640e29e224
Revises: 7f2faebd2013
Create Date: 2017-10-04 17:12:28.857308

"""
import os

from alembic import op
import sqlalchemy as sa


schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = '20640e29e224'
down_revision = '7f2faebd2013'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'celebrity_follow',
        sa.Column('_id', sa.Text, nullable=False, unique=True),
        sa.Column('_database_id', sa.Text, nullable=False),
        sa.Column('_owner_id', sa.Text, nullable=False),
        sa.Column('_access', sa.dialects.postgresql.JSONB),
        sa.Column('_created_by', sa.Text),
        sa.Column('_created_at', sa.DateTime, nullable=False),
        sa.Column('_updated_by', sa.Text),
        sa.Column('_updated_at', sa.DateTime, nullable=False),
        sa.Column('user_id', sa.Text, nullable=False),
        sa.Column('celebrity_id', sa.Text, nullable=False),
        sa.PrimaryKeyConstraint('_id', '_database_id', '_owner_id'),
        sa.UniqueConstraint('user_id', 'celebrity_id'),
        sa.ForeignKeyConstraint(['user_id'], ['%s.user._id' % schema_name]),
        sa.ForeignKeyConstraint(['celebrity_id'], ['%s.celebrity._id' % schema_name]),
        schema=schema_name
    )

    op.execute(
    """
    CREATE TRIGGER trigger_notify_record_change
    AFTER INSERT OR UPDATE OR DELETE
    ON %s.celebrity_follow
    FOR EACH ROW
    EXECUTE PROCEDURE public.notify_record_change();
    """ % schema_name
    )


def downgrade():
    op.drop_table('celebrity_follow', schema=schema_name)

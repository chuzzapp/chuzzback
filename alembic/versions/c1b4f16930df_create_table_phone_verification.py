"""create table phone verification

Revision ID: c1b4f16930df
Revises: 654eebb248a8
Create Date: 2017-10-10 16:27:13.359160

"""
import os

from alembic import op
import sqlalchemy as sa


schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = 'c1b4f16930df'
down_revision = '654eebb248a8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'phone_verification',
        sa.Column('_id', sa.Text, nullable=False, unique=True),
        sa.Column('_database_id', sa.Text, nullable=False),
        sa.Column('_owner_id', sa.Text, nullable=False),
        sa.Column('_access', sa.dialects.postgresql.JSONB),
        sa.Column('_created_by', sa.Text),
        sa.Column('_created_at', sa.DateTime, nullable=False),
        sa.Column('_updated_by', sa.Text),
        sa.Column('_updated_at', sa.DateTime, nullable=False),

        sa.Column('number', sa.Text, nullable=False),
        sa.Column('country_code', sa.Text, nullable=False),
        sa.Column('revoked', sa.Boolean, nullable=False),
        sa.Column('code', sa.Text, nullable=False),
        sa.Column('expired_at', sa.DateTime, nullable=False),

        sa.PrimaryKeyConstraint('_id', '_database_id', '_owner_id'),
        schema=schema_name
    )

    op.execute(
        """
        CREATE TRIGGER trigger_notify_record_change
        AFTER INSERT OR UPDATE OR DELETE
        ON %s.phone_verification
        FOR EACH ROW
        EXECUTE PROCEDURE public.notify_record_change();
        """ % schema_name
    )


def downgrade():
    op.drop_table('phone_verification', schema=schema_name)

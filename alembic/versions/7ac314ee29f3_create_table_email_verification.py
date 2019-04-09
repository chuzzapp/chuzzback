"""create table email verification

Revision ID: 7ac314ee29f3
Revises: 6c60ebf42695
Create Date: 2017-10-23 17:59:17.430380

"""
import os

from alembic import op
import sqlalchemy as sa


schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = '7ac314ee29f3'
down_revision = '6c60ebf42695'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'email_verification',
        sa.Column('_id', sa.Text, nullable=False, unique=True),
        sa.Column('_database_id', sa.Text, nullable=False),
        sa.Column('_owner_id', sa.Text, nullable=False),
        sa.Column('_access', sa.dialects.postgresql.JSONB),
        sa.Column('_created_by', sa.Text),
        sa.Column('_created_at', sa.DateTime, nullable=False),
        sa.Column('_updated_by', sa.Text),
        sa.Column('_updated_at', sa.DateTime, nullable=False),

        sa.Column('email', sa.Text, nullable=False),
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
        ON %s.email_verification
        FOR EACH ROW
        EXECUTE PROCEDURE public.notify_record_change();
        """ % schema_name
    )


def downgrade():
    op.drop_table('email_verification', schema=schema_name)

"""create table answer

Revision ID: 4fb303432112
Revises: e9f303d37c98
Create Date: 2017-10-04 15:53:08.288930

"""
import os

from alembic import op
import sqlalchemy as sa


schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = '4fb303432112'
down_revision = 'e9f303d37c98'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'answer',
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
        sa.Column('question_id', sa.Text, nullable=False),
        sa.Column('selected_choice_id', sa.Text, nullable=False),
        sa.PrimaryKeyConstraint('_id', '_database_id', '_owner_id'),
        sa.UniqueConstraint('user_id', 'poll_id'),
        sa.ForeignKeyConstraint(['user_id'], ['%s.user._id' % schema_name]),
        sa.ForeignKeyConstraint(['poll_id'], ['%s.poll._id' % schema_name]),
        sa.ForeignKeyConstraint(['question_id'], ['%s.question._id' % schema_name]),
        sa.ForeignKeyConstraint(['selected_choice_id'], ['%s.choice._id' % schema_name]),
        schema=schema_name
    )

    op.execute(
    """
    CREATE TRIGGER trigger_notify_record_change
    AFTER INSERT OR UPDATE OR DELETE
    ON %s.answer
    FOR EACH ROW
    EXECUTE PROCEDURE public.notify_record_change();
    """ % schema_name
    )


def downgrade():
    op.drop_table('answer', schema=schema_name)

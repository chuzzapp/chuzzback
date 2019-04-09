"""create table poll country

Revision ID: b4364f33391d
Revises: 9392809b1fe6
Create Date: 2018-01-24 14:04:57.053937

"""
import os

from alembic import op
import sqlalchemy as sa
from uuid import uuid4
from datetime import datetime


schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = 'b4364f33391d'
down_revision = '9392809b1fe6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'poll_country',
        sa.Column('_id', sa.Text, nullable=False, unique=True),
        sa.Column('_database_id', sa.Text, nullable=False),
        sa.Column('_owner_id', sa.Text, nullable=False),
        sa.Column('_access', sa.dialects.postgresql.JSONB),
        sa.Column('_created_by', sa.Text, nullable=False),
        sa.Column('_created_at', sa.DateTime),
        sa.Column('_updated_by', sa.Text, nullable=False),
        sa.Column('_updated_at', sa.DateTime),
        sa.Column('poll_id', sa.Text, nullable=False),
        sa.Column('country_id', sa.Text, nullable=False),
        sa.PrimaryKeyConstraint('_id', '_database_id', '_owner_id'),
        sa.UniqueConstraint('poll_id', 'country_id'),
        sa.ForeignKeyConstraint(['poll_id'], ['%s.poll._id' % schema_name]),
        sa.ForeignKeyConstraint(['country_id'], ['%s.country._id' % schema_name]),
        schema=schema_name
    )

    op.execute(
        """
        CREATE TRIGGER trigger_notify_record_change
        AFTER INSERT OR UPDATE OR DELETE
        ON %s.poll_country
        FOR EACH ROW
        EXECUTE PROCEDURE public.notify_record_change();
        """ % schema_name
    )

    conn = op.get_bind()
    query_result = conn.execute(
        '''
            SELECT _id, country_id FROM {schema}.poll
            WHERE country_id IS NOT NULL
        '''.format(schema=schema_name)
    )

    for result in query_result:
        poll_id = result[0]
        country_id = result[1]
        conn.execute(
            '''
            INSERT INTO {schema}.poll_country (_id, _database_id, _owner_id, _access, _created_by, _created_at, _updated_by, _updated_at, poll_id, country_id) VALUES
            ('{id}', '', '', NULL, '', '{created_at}', '', '{created_at}', '{poll_id}', '{country_id}')
            '''.format(schema=schema_name, id=str(uuid4()), created_at=datetime.utcnow(), poll_id=poll_id, country_id=country_id)
        )

    op.drop_constraint('poll_country__id', 'poll', schema='%s' % schema_name)

    with op.batch_alter_table("poll", schema=schema_name) as batch_op:
        batch_op.drop_column('country_id')


def downgrade():
    with op.batch_alter_table("poll", schema=schema_name) as batch_op:
        batch_op.add_column(
            sa.Column('country_id', sa.Text))

    op.create_foreign_key(
        'poll_country__id', 'poll', 'country',
        ['country_id'], ['_id'], source_schema='%s' % schema_name, referent_schema='%s' % schema_name)

    conn = op.get_bind()
    poll_country_list = conn.execute(
        '''
            SELECT DISTINCT ON (poll_id) poll_id, country_id FROM {schema}.poll_country;
        '''.format(schema=schema_name)
    )

    for poll_country in poll_country_list:
        poll_id = poll_country[0]
        country_id = poll_country[1]
        conn.execute(
            '''
            UPDATE {schema}.poll
            SET country_id = '{country_id}'
            WHERE _id = '{poll_id}'
            '''.format(schema=schema_name, poll_id=poll_id, country_id=country_id)
        )

    op.drop_table('poll_country', schema=schema_name)

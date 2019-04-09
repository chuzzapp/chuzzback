"""migrate various count value

Revision ID: e2b742369866
Revises: 2da4a547556f
Create Date: 2017-11-13 10:51:02.596141

"""
import os

from alembic import op
import sqlalchemy as sa

schema_name = os.getenv('SCHEMA_NAME')

# revision identifiers, used by Alembic.
revision = 'e2b742369866'
down_revision = '2da4a547556f'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        '''
            UPDATE {schema}.user u
            SET
            answers_count = (
                SELECT COUNT(DISTINCT(a.poll_id)) FROM {schema}.answer a
                WHERE a.user_id = u._id
            ),
            groups_count = 0,
            likes_count = 0,
            polls_count = (
                SELECT COUNT(p._id) FROM {schema}.poll p
                WHERE p.user_id = u._id
            ),
            followers_count = (
                SELECT count(f._id) FROM {schema}.celebrity_follow f
                JOIN {schema}.celebrity c ON c._id = f.celebrity_id
                WHERE c._id = u._id
            ),
            following_count = (
                SELECT COUNT(f._id) FROM {schema}.celebrity_follow f
                WHERE f.user_id = u._id
            )
        '''.format(schema=schema_name)
    )

    op.execute(
        '''
            UPDATE {schema}.celebrity c
            SET
            followers_count = (
                SELECT count(f._id) FROM {schema}.celebrity_follow f
                WHERE c._id = f.celebrity_id
            )
        '''.format(schema=schema_name)
    )

    op.execute(
        '''
            UPDATE {schema}.poll p
            SET
            answers = (
                SELECT COUNT(DISTINCT(a.user_id)) FROM {schema}.answer a
                WHERE a.poll_id = p._id
            )
        '''.format(schema=schema_name)
    )


def downgrade():
    pass

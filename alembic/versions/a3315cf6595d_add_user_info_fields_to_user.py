"""add user info fields to user

Revision ID: a3315cf6595d
Revises:
Create Date: 2017-10-04 11:51:58.286117

"""

import os

from alembic import op
import sqlalchemy as sa


schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = 'a3315cf6595d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("user", schema=schema_name) as batch_op:
        batch_op.add_column(
            sa.Column('phone_number', sa.Text))
        batch_op.add_column(
            sa.Column('birthday', sa.DateTime))
        batch_op.add_column(
            sa.Column('gender', sa.Text))
        batch_op.add_column(
            sa.Column('sexual_preference', sa.Text))
        batch_op.add_column(
            sa.Column('country', sa.Text))
        batch_op.add_column(
            sa.Column('selected_topics', sa.dialects.postgresql.JSONB))
        batch_op.add_column(
            sa.Column('image_id', sa.Text))
    op.create_foreign_key(
        'user__asset_id', 'user', '_asset',
        ['image_id'], ['id'], source_schema='%s' % schema_name, referent_schema='%s' % schema_name)
    op.create_check_constraint("constraint_check_gender", "user", "gender = ANY(ARRAY['male', 'female', 'other'])", schema=schema_name)
    op.create_check_constraint("constraint_check_sexual_preference", "user", "sexual_preference = ANY(ARRAY['heterosexual', 'homosexual', 'bisexual'])", schema=schema_name)


def downgrade():
    op.drop_constraint('user__asset_id', 'user', schema='%s' % schema_name)
    op.drop_constraint("constraint_check_gender", "user", type_="check", schema=schema_name)
    op.drop_constraint("constraint_check_sexual_preference", "user", type_="check", schema=schema_name)
    with op.batch_alter_table("user", schema=schema_name) as batch_op:
        batch_op.drop_column('phone_number')
        batch_op.drop_column('birthday')
        batch_op.drop_column('gender')
        batch_op.drop_column('sexual_preference')
        batch_op.drop_column('country')
        batch_op.drop_column('selected_topics')
        batch_op.drop_column('image_id')

"""fix unique constraint of answer

Revision ID: b87a5228ede5
Revises: cb418a6e7921
Create Date: 2017-11-07 18:11:53.274553

"""
import os

from alembic import op
import sqlalchemy as sa


schema_name = os.getenv('SCHEMA_NAME')


# revision identifiers, used by Alembic.
revision = 'b87a5228ede5'
down_revision = 'cb418a6e7921'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint('answer_user_id_poll_id_key', 'answer', schema='%s' % schema_name)
    op.create_unique_constraint('answer_user_id_question_id_selected_choice_id_key', 'answer', ['user_id', 'question_id', 'selected_choice_id'], schema='%s' % schema_name)


def downgrade():
    op.create_unique_constraint('answer_user_id_poll_id_key', 'answer', ['poll_id', 'user_id'], schema='%s' % schema_name)
    op.drop_constraint('answer_user_id_question_id_selected_choice_id_key', 'answer', schema='%s' % schema_name)

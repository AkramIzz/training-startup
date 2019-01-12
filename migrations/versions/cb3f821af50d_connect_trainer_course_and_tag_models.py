"""Connect Trainer , Course and Tag models

Revision ID: cb3f821af50d
Revises: 579698981da4
Create Date: 2019-01-12 15:23:38.893488

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'cb3f821af50d'
down_revision = '579698981da4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('course', sa.Column('tag_id', sa.Integer(), nullable=True))
    op.add_column('course', sa.Column('trainer_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'course', 'user', ['trainer_id'], ['id'])
    op.create_foreign_key(None, 'course', 'tag', ['tag_id'], ['id'])
    op.drop_column('course', 'category')
    op.drop_column('course', 'trainer')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('course', sa.Column('trainer', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=120), nullable=True))
    op.add_column('course', sa.Column('category', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=120), nullable=True))
    op.drop_constraint(None, 'course', type_='foreignkey')
    op.drop_constraint(None, 'course', type_='foreignkey')
    op.drop_column('course', 'trainer_id')
    op.drop_column('course', 'tag_id')
    # ### end Alembic commands ###

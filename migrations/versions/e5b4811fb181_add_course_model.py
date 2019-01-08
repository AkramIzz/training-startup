"""Add Course model

Revision ID: e5b4811fb181
Revises: 19c4fbdb1a0b
Create Date: 2019-01-08 20:53:52.298413

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5b4811fb181'
down_revision = '19c4fbdb1a0b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('course',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('category', sa.String(length=120), nullable=True),
    sa.Column('trainer', sa.String(length=120), nullable=True),
    sa.Column('goals', sa.String(length=1600), nullable=True),
    sa.Column('outlines', sa.String(length=1600), nullable=True),
    sa.Column('prerequists', sa.String(length=300), nullable=True),
    sa.Column('target', sa.String(length=300), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('duration', sa.String(length=100), nullable=True),
    sa.Column('time', sa.String(length=100), nullable=True),
    sa.Column('fees', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('course')
    # ### end Alembic commands ###

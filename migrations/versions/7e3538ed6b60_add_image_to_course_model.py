"""Add image to course model

Revision ID: 7e3538ed6b60
Revises: 3001345478e9
Create Date: 2019-02-23 14:56:54.738793

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e3538ed6b60'
down_revision = '3001345478e9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('course', sa.Column('image', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('course', 'image')
    # ### end Alembic commands ###

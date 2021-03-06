"""Add image to User model

Revision ID: 39686d60064b
Revises: cb3f821af50d
Create Date: 2019-01-19 18:50:44.228224

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39686d60064b'
down_revision = 'cb3f821af50d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('image', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'image')
    # ### end Alembic commands ###

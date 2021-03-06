"""user_media model for storing media files metadata

Revision ID: 19c4fbdb1a0b
Revises: 86b60c529d09
Create Date: 2019-01-08 18:41:41.894158

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19c4fbdb1a0b'
down_revision = '86b60c529d09'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_media',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('filename', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_media_filename'), 'user_media', ['filename'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_media_filename'), table_name='user_media')
    op.drop_table('user_media')
    # ### end Alembic commands ###

"""user and all (four) user types tables

Revision ID: 411342591abe
Revises: 
Create Date: 2019-01-05 16:08:57.485781

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '411342591abe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('fullname', sa.String(length=120), nullable=True),
    sa.Column('gender', sa.Boolean(), nullable=True),
    sa.Column('activated', sa.Boolean(), nullable=True),
    sa.Column('phone', sa.String(length=16), nullable=True),
    sa.Column('birthdate', sa.Date(), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('user_type', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('lecture_room',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('room_name', sa.String(length=180), nullable=True),
    sa.Column('address', sa.String(length=180), nullable=True),
    sa.Column('fees', sa.Integer(), nullable=True),
    sa.Column('chairs', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('trainee',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('academic_level', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('trainer',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('specialization', sa.String(length=180), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('training_center',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('center_name', sa.String(length=180), nullable=True),
    sa.Column('specialization', sa.String(length=180), nullable=True),
    sa.Column('address', sa.String(length=180), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('training_center')
    op.drop_table('trainer')
    op.drop_table('trainee')
    op.drop_table('lecture_room')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
"""empty message

Revision ID: e8a99f0ea171
Revises: 779d7b565aba
Create Date: 2022-11-13 17:22:31.683611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8a99f0ea171'
down_revision = '779d7b565aba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('add_date', sa.DateTime(), nullable=False),
    sa.Column('pub_date', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=128), nullable=False),
    sa.Column('password', sa.String(length=320), nullable=False),
    sa.Column('avatar', sa.String(length=200), nullable=True),
    sa.Column('is_super_user', sa.Boolean(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_staff', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###

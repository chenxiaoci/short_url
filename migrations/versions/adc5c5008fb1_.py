"""empty message

Revision ID: adc5c5008fb1
Revises: f66e46b0e069
Create Date: 2018-07-15 22:43:48.086391

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'adc5c5008fb1'
down_revision = 'f66e46b0e069'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('_uuid', sa.String(length=64), nullable=True),
    sa.Column('nick_name', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=30), nullable=True),
    sa.Column('_password', sa.String(length=128), nullable=True),
    sa.Column('confirm', sa.Boolean(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###

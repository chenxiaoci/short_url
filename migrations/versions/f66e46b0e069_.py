"""empty message

Revision ID: f66e46b0e069
Revises: a50b89a8f82e
Create Date: 2018-07-13 20:29:16.987908

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f66e46b0e069'
down_revision = 'a50b89a8f82e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('url', sa.Column('create_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('url', 'create_time')
    # ### end Alembic commands ###
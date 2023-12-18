"""delete total from session

Revision ID: 2e8212fb61de
Revises: fbfb53920d58
Create Date: 2023-12-18 15:43:45.975031

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e8212fb61de'
down_revision = 'fbfb53920d58'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('session', schema=None) as batch_op:
        batch_op.drop_column('total')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('session', schema=None) as batch_op:
        batch_op.add_column(sa.Column('total', sa.FLOAT(), nullable=False))

    # ### end Alembic commands ###
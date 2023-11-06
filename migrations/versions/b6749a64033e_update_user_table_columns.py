"""update User table columns

Revision ID: b6749a64033e
Revises: b633602a4e65
Create Date: 2023-11-06 16:11:55.194841

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6749a64033e'
down_revision = 'b633602a4e65'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fullname', sa.String(length=60), nullable=True))
        batch_op.add_column(sa.Column('gender', sa.CHAR(length=1), nullable=True))
        batch_op.add_column(sa.Column('telephone', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('telephone')
        batch_op.drop_column('gender')
        batch_op.drop_column('fullname')

    # ### end Alembic commands ###
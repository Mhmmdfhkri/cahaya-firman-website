""" add address User table columns

Revision ID: 060efd2b3aef
Revises: b6749a64033e
Create Date: 2023-11-06 21:06:11.370315

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '060efd2b3aef'
down_revision = 'b6749a64033e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('address', sa.String(length=60), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('address')

    # ### end Alembic commands ###

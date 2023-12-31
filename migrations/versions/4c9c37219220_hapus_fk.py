"""hapus fk

Revision ID: 4c9c37219220
Revises: fc759a371c4f
Create Date: 2023-11-14 19:20:13.300815

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c9c37219220'
down_revision = 'fc759a371c4f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payment_detail', schema=None) as batch_op:
        batch_op.drop_column('payment_methodsss')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payment_detail', schema=None) as batch_op:
        batch_op.add_column(sa.Column('payment_methodsss', sa.VARCHAR(length=100), nullable=True))

    # ### end Alembic commands ###

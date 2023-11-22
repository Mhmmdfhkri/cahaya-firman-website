"""fix session

Revision ID: 636ee2468b8e
Revises: 25cdaaeb4abd
Create Date: 2023-11-14 20:51:39.188422

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '636ee2468b8e'
down_revision = '25cdaaeb4abd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('session', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.Boolean(), nullable=True))
        batch_op.alter_column('id_user',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('session', schema=None) as batch_op:
        batch_op.alter_column('id_user',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.drop_column('is_active')

    # ### end Alembic commands ###
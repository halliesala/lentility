"""empty message

Revision ID: 7a39a4958a06
Revises: bd1f9827a61b
Create Date: 2023-10-06 10:46:00.419485

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a39a4958a06'
down_revision = 'bd1f9827a61b'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_heartysoupsinternational():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('shipping_cost', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade_heartysoupsinternational():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('shipping_cost')

    # ### end Alembic commands ###


def upgrade_planterson():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('shipping_cost', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade_planterson():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('shipping_cost')

    # ### end Alembic commands ###


def upgrade_lentsplysproutona():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('shipping_cost', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade_lentsplysproutona():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('shipping_cost')

    # ### end Alembic commands ###


def upgrade_lentilcity():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('shipping_cost', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade_lentilcity():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('shipping_cost')

    # ### end Alembic commands ###


def upgrade_dclentil():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('shipping_cost', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade_dclentil():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('shipping_cost')

    # ### end Alembic commands ###


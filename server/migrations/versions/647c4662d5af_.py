"""empty message

Revision ID: 647c4662d5af
Revises: 02e9f1d17a5a
Create Date: 2023-10-10 17:49:12.577774

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '647c4662d5af'
down_revision = '02e9f1d17a5a'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('canonical_products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quantity', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('canonical_products', schema=None) as batch_op:
        batch_op.drop_column('quantity')

    # ### end Alembic commands ###


def upgrade_heartysoupsinternational():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_heartysoupsinternational():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_planterson():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_planterson():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_lentsplysproutona():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_lentsplysproutona():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_lentilcity():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_lentilcity():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_dclentil():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_dclentil():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

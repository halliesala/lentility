"""empty message

Revision ID: 80b7bbb04b44
Revises: 
Create Date: 2023-10-03 15:09:26.296477

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80b7bbb04b44'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('addresses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('practice_id', sa.Integer(), nullable=True),
    sa.Column('line_1', sa.String(), nullable=False),
    sa.Column('line_2', sa.String(), nullable=True),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('state', sa.String(), nullable=False),
    sa.Column('zip_code', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['practice_id'], ['practices.id'], name=op.f('fk_addresses_practice_id_practices')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('manufacturers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('practices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('primary_user_id', sa.Integer(), nullable=True),
    sa.Column('primary_shipping_address_id', sa.Integer(), nullable=True),
    sa.Column('primary_billing_address_id', sa.Integer(), nullable=True),
    sa.Column('created_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['primary_billing_address_id'], ['addresses.id'], name=op.f('fk_practices_primary_billing_address_id_addresses')),
    sa.ForeignKeyConstraint(['primary_shipping_address_id'], ['addresses.id'], name=op.f('fk_practices_primary_shipping_address_id_addresses')),
    sa.ForeignKeyConstraint(['primary_user_id'], ['users.id'], name=op.f('fk_practices_primary_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('suppliers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('website', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('practice_id', sa.Integer(), nullable=True),
    sa.Column('role', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['practice_id'], ['practices.id'], name=op.f('fk_users_practice_id_practices')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('canonical_products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('manufacturer_id', sa.Integer(), nullable=True),
    sa.Column('manufacturer_sku', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('image_link', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['manufacturer_id'], ['manufacturers.id'], name=op.f('fk_canonical_products_manufacturer_id_manufacturers')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payment_methods',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('practice_id', sa.Integer(), nullable=True),
    sa.Column('billing_address_id', sa.Integer(), nullable=True),
    sa.Column('nickname', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['billing_address_id'], ['addresses.id'], name=op.f('fk_payment_methods_billing_address_id_addresses')),
    sa.ForeignKeyConstraint(['practice_id'], ['practices.id'], name=op.f('fk_payment_methods_practice_id_practices')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('supplier_accounts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('supplier_id', sa.Integer(), nullable=True),
    sa.Column('practice_id', sa.Integer(), nullable=True),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('valid', sa.Boolean(), nullable=False),
    sa.Column('last_validated', sa.DateTime(), nullable=True),
    sa.Column('created_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['practice_id'], ['practices.id'], name=op.f('fk_supplier_accounts_practice_id_practices')),
    sa.ForeignKeyConstraint(['supplier_id'], ['suppliers.id'], name=op.f('fk_supplier_accounts_supplier_id_suppliers')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('practice_id', sa.Integer(), nullable=True),
    sa.Column('placed_by_user_id', sa.Integer(), nullable=True),
    sa.Column('created_time', sa.DateTime(), nullable=False),
    sa.Column('placed_time', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('payment_method_id', sa.Integer(), nullable=True),
    sa.Column('shipping_address_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['payment_method_id'], ['payment_methods.id'], name=op.f('fk_orders_payment_method_id_payment_methods')),
    sa.ForeignKeyConstraint(['placed_by_user_id'], ['users.id'], name=op.f('fk_orders_placed_by_user_id_users')),
    sa.ForeignKeyConstraint(['practice_id'], ['practices.id'], name=op.f('fk_orders_practice_id_practices')),
    sa.ForeignKeyConstraint(['shipping_address_id'], ['addresses.id'], name=op.f('fk_orders_shipping_address_id_addresses')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('canonical_product_id', sa.Integer(), nullable=True),
    sa.Column('supplier_id', sa.Integer(), nullable=True),
    sa.Column('supplier_sku', sa.String(), nullable=False),
    sa.Column('image_link', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['canonical_product_id'], ['canonical_products.id'], name=op.f('fk_products_canonical_product_id_canonical_products')),
    sa.ForeignKeyConstraint(['supplier_id'], ['suppliers.id'], name=op.f('fk_products_supplier_id_suppliers')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vendor_orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('supplier_id', sa.Integer(), nullable=True),
    sa.Column('shipping_and_handling', sa.Float(), nullable=False),
    sa.Column('tax', sa.Float(), nullable=False),
    sa.Column('tracking_number', sa.String(), nullable=True),
    sa.Column('estimated_delivery_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], name=op.f('fk_vendor_orders_order_id_orders')),
    sa.ForeignKeyConstraint(['supplier_id'], ['suppliers.id'], name=op.f('fk_vendor_orders_supplier_id_suppliers')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('fulfilled_by_product_id', sa.Integer(), nullable=True),
    sa.Column('created_time', sa.DateTime(), nullable=False),
    sa.Column('canonical_product_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('vendor_order_id', sa.Integer(), nullable=True),
    sa.Column('disposition', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['canonical_product_id'], ['canonical_products.id'], name=op.f('fk_order_items_canonical_product_id_canonical_products')),
    sa.ForeignKeyConstraint(['fulfilled_by_product_id'], ['products.id'], name=op.f('fk_order_items_fulfilled_by_product_id_products')),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], name=op.f('fk_order_items_order_id_orders')),
    sa.ForeignKeyConstraint(['vendor_order_id'], ['vendor_orders.id'], name=op.f('fk_order_items_vendor_order_id_vendor_orders')),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_items')
    op.drop_table('vendor_orders')
    op.drop_table('products')
    op.drop_table('orders')
    op.drop_table('supplier_accounts')
    op.drop_table('payment_methods')
    op.drop_table('canonical_products')
    op.drop_table('users')
    op.drop_table('suppliers')
    op.drop_table('practices')
    op.drop_table('manufacturers')
    op.drop_table('addresses')
    # ### end Alembic commands ###

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    canonical_product_id = db.Column(db.Integer, db.ForeignKey('canonical_products.id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    supplier_sku = db.Column(db.String, nullable=False)
    image_link = db.Column(db.String)

class CanonicalProduct(db.Model, SerializerMixin):
    __tablename__ = 'canonical_products'

    id = db.Column(db.Integer, primary_key=True)
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturers.id'))
    manufacturer_sku = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    image_link = db.Column(db.String)

class Manufacturer(db.Model, SerializerMixin):
    __tablename__ = 'manufacturers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

class Supplier(db.Model, SerializerMixin):
    __tablename__ = 'suppliers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    website = db.Column(db.String, nullable=False)

class SupplierAccount(db.Model, SerializerMixin):
    __tablename__ = 'supplier_accounts'

    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    practice_id = db.Column(db.Integer, db.ForeignKey('practices.id'))
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    valid = db.Column(db.Boolean, nullable=False)
    last_validated = db.Column(db.DateTime)
    created_time = db.Column(db.DateTime, nullable=False)
    
class Practice(db.Model, SerializerMixin):
    __tablename__ = 'practices'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    primary_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    primary_shipping_address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'))
    primary_billing_address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'))
    created_time = db.Column(db.DateTime, nullable=False)

class Address(db.Model, SerializerMixin):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    practice_id = db.Column(db.Integer, db.ForeignKey('practices.id'))
    line_1 = db.Column(db.String, nullable=False)
    line_2 = db.Column(db.String)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    zip_code = db.Column(db.String, nullable=False)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String)
    practice_id = db.Column(db.Integer, db.ForeignKey('practices.id'))
    role = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    
class Order(db.Model, SerializerMixin):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    practice_id = db.Column(db.Integer, db.ForeignKey('practices.id'))
    placed_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_time = db.Column(db.DateTime, nullable=False)
    placed_time = db.Column(db.DateTime)
    status = db.Column(db.String, nullable=False)
    payment_method_id = db.Column(db.Integer, db.ForeignKey('payment_methods.id'))
    shipping_address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'))

class OrderItem(db.Model, SerializerMixin):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    fulfilled_by_product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    created_time = db.Column(db.DateTime, nullable=False)
    canonical_product_id = db.Column(db.Integer, db.ForeignKey('canonical_products.id'))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    vendor_order_id = db.Column(db.Integer, db.ForeignKey('vendor_orders.id'))
    disposition = db.Column(db.String, nullable=False)

class VendorOrders(db.Model, SerializerMixin):
    __tablename__ = 'vendor_orders'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    shipping_and_handling = db.Column(db.Float, nullable=False)
    tax = db.Column(db.Float, nullable=False)
    tracking_number = db.Column(db.String)
    estimated_delivery_date = db.Column(db.DateTime)

class PaymentMethod(db.Model, SerializerMixin):
    __tablename__ = 'payment_methods'
    
    id = db.Column(db.Integer, primary_key=True)
    practice_id = db.Column(db.Integer, db.ForeignKey('practices.id'))
    billing_address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'))
    nickname = db.Column(db.String)


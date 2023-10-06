from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

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

    # Relationships #
    # canonical_product = db.relationship('CanonicalProduct', backref='products')
    # supplier = db.relationship('Supplier', backref='products')

    # Validations #
    # -- Supplier SKUs must be unique for each supplier
    # @validates('supplier_sku')
    # def validate_supplier_sku(self, key, supplier_sku):
    #     assert not Product.query.filter_by(supplier_id=self.supplier_id, supplier_sku=supplier_sku).first()
    #     return supplier_sku
    # # -- Each supplier can have at most one product for each canonical product
    # @validates('canonical_product_id')
    # def validate_canonical_product_id(self, key, canonical_product_id):
    #     assert not Product.query.filter_by(supplier_id=self.supplier_id, canonical_product_id=canonical_product_id).first()
    #     return canonical_product_id

    
class CanonicalProduct(db.Model, SerializerMixin):
    __tablename__ = 'canonical_products'

    id = db.Column(db.Integer, primary_key=True)
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturers.id'))
    manufacturer_sku = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    image_link = db.Column(db.String)
    quantity = db.Column(db.Integer)

    # 'Core price' for product. Suppliers will charge a markup on this price, and also randomly vary price by practice.
    price_preset = db.Column(db.Float)

    # Relationships #
    # products = db.relationship('Product', backref='canonical_product')
    # manufacturer = db.relationship('Manufacturer', backref='canonical_products')

    # Validations #
    # -- Manufacturer SKUs must be unique for each manufacturer
    # @validates('manufacturer_sku')
    # def validate_manufacturer_sku(self, key, manufacturer_sku):
    #     assert not CanonicalProduct.query.filter_by(manufacturer_id=self.manufacturer_id, manufacturer_sku=manufacturer_sku).first()
    #     return manufacturer_sku


class Manufacturer(db.Model, SerializerMixin):
    __tablename__ = 'manufacturers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    # Relationships #
    # canonical_products = db.relationship('CanonicalProduct', backref='manufacturer')
    # products = association_proxy('canonical_products', 'products')

class Supplier(db.Model, SerializerMixin):
    __tablename__ = 'suppliers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    house_brand = db.Column(db.String, nullable=False)
    preferred = db.Column(db.Boolean, nullable=False)

    # # Relationships
    # products = db.relationship('Product', backref='supplier')
    # supplier_accounts = db.relationship('SupplierAccount', backref='supplier')
    # vendor_orders = db.relationship('VendorOrders', backref='supplier')

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

    # # Relationships #
    # supplier = db.relationship('Supplier', backref='supplier_accounts')
    # practice = db.relationship('Practice', backref='supplier_accounts')

    # # Potential Validations #
    # # -- Only one account is allowed for each supplier/practice pair
    
    
class Practice(db.Model, SerializerMixin):
    __tablename__ = 'practices'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    created_time = db.Column(db.DateTime, nullable=False)

    # # Relationships #
    # supplier_accounts = db.relationship('SupplierAccount', backref='practice')
    # suppliers = association_proxy('supplier_accounts', 'supplier')
    # users = db.relationship('User', backref='practice')
    # addresses = db.relationship('Address', backref='practice')
    # orders = db.relationship('Order', backref='practice')

class Address(db.Model, SerializerMixin):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    practice_id = db.Column(db.Integer, db.ForeignKey('practices.id'))
    line_1 = db.Column(db.String, nullable=False)
    line_2 = db.Column(db.String)
    city = db.Column(db.String, nullable=False)
    us_state = db.Column(db.String, nullable=False)
    zip_code = db.Column(db.String, nullable=False)
    is_primary_shipping = db.Column(db.Boolean, nullable=False)

    # # Relationships #
    # practice = db.relationship('Practice', backref='addresses')
    # orders = db.relationship('Order', backref='shipping_address')

    # # Validations #

    # # Only one primary shipping address is allowed for each practice #
    # @validates('is_primary_shipping')
    # def validate_is_primary_shipping(self, key, is_primary_shipping):
    #     if is_primary_shipping:
    #         assert not Address.query.filter_by(practice_id=self.practice_id, is_primary_shipping=True).first()
    #     return is_primary_shipping
    
    

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String)
    practice_id = db.Column(db.Integer, db.ForeignKey('practices.id'))
    role = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    is_primary = db.Column(db.Boolean, nullable=False)

    # # Relationships #
    # practice = db.relationship('Practice', backref='users')
    # orders = db.relationship('Order', backref='placed_by_user')

    # # Validations #
    # # -- Only one primary user is allowed for each practice #
    # @validates('is_primary')
    # def validate_is_primary(self, key, is_primary):
    #     if is_primary:
    #         assert not User.query.filter_by(practice_id=self.practice_id, is_primary=True).first()
    #     return is_primary
    # # -- Allowed roles: admin, lentist, lentil_assistant
    # @validates('role')
    # def validate_role(self, key, role):
    #     assert role in ['admin', 'lentist', 'lentil_assistant']
    #     return role
    
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

    # # Relationships #
    # practice = db.relationship('Practice', backref='orders')
    # placed_by_user = db.relationship('User', foreign_keys=[placed_by_user_id], post_update=True)
    # payment_method = db.relationship('PaymentMethod', backref='orders')
    # shipping_address = db.relationship('Address', backref='orders')
    # order_items = db.relationship('OrderItem', backref='order')
    # vendor_orders = db.relationship('VendorOrders', backref='order')

    # Validations #
    # Status can be 'in_cart', 'placed', 'delivered'
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

    # # Relationships #
    # order = db.relationship('Order', backref='order_items')
    # fulfilled_by_product = db.relationship('Product', foreign_keys=[fulfilled_by_product_id], post_update=True)
    # canonical_product = db.relationship('CanonicalProduct', foreign_keys=[canonical_product_id], post_update=True)
    # vendor_order = db.relationship('VendorOrders', backref='order_items')

class VendorOrder(db.Model, SerializerMixin):
    __tablename__ = 'vendor_orders'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    shipping_and_handling = db.Column(db.Float, nullable=False)
    tax = db.Column(db.Float, nullable=False)
    tracking_number = db.Column(db.String)
    estimated_delivery_date = db.Column(db.DateTime)

    # # Relationships #
    # order = db.relationship('Order', backref='vendor_orders')
    # order_items = db.relationship('OrderItem', backref='vendor_order')
    # supplier = db.relationship('Supplier', backref='vendor_orders')

class PaymentMethod(db.Model, SerializerMixin):
    __tablename__ = 'payment_methods'

    id = db.Column(db.Integer, primary_key=True)
    practice_id = db.Column(db.Integer, db.ForeignKey('practices.id'))
    billing_address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'))
    nickname = db.Column(db.String)
    is_primary = db.Column(db.Boolean)

    # # Relationships #
    # orders = db.relationship('Order', backref='payment_method')
    # practice = db.relationship('Practice', backref='payment_methods')
    # billing_address = db.relationship('Address', foreign_keys=[billing_address_id], post_update=True)


# Abstract classes for vendor dbs #
class VendorUser(db.Model, SerializerMixin):
    __abstract__ = True
    __tablename__ = 'users'


    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    # Practice-specific discount or markup of up to 20%
    price_multiplier = db.Column(db.Float, nullable=False)
    days_to_ship = db.Column(db.Integer, nullable=False)

class VendorProduct(db.Model, SerializerMixin):
    __abstract__ = True
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    sku = db.Column(db.String, nullable=False)
    manufacturer_name = db.Column(db.String, nullable=False)
    manufacturer_sku = db.Column(db.String, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image_link = db.Column(db.String)
    # This is the core price; vendors will also randomly vary prices by practice
    price_preset = db.Column(db.Float, nullable=False)


# Dynamically create the tables for each vendor
VENDORS = ['heartysoupsinternational', 'planterson', 'lentsplysproutona', 'lentilcity', 'dclentil']
TABLES_AND_CLASSES = [('user', VendorUser), ('product', VendorProduct)]
vendor_classes = {}
for v in VENDORS:
    for (t, c) in TABLES_AND_CLASSES:
        globals()[f"{v.capitalize()}{t.capitalize()}"] = type(f"{v.capitalize()}{t.capitalize()}", (c,), {'__bind_key__': v})
        vendor_classes[f"{v.capitalize()}{t.capitalize()}"] = globals()[f"{v.capitalize()}{t.capitalize()}"]
        
        # ChatGPT generated the code below; I rewrote it with the second 'for' loop
        # globals()[f"{vendor.capitalize()}User"] = type(f"{vendor.capitalize()}User", (VendorUser,), {'__bind_key__': vendor})
        # globals()[f"{vendor.capitalize()}Product"] = type(f"{vendor.capitalize()}Product", (VendorProduct,), {'__bind_key__': vendor})
        # globals()[f"{vendor.capitalize()}Prices"] = type(f"{vendor.capitalize()}Prices", (VendorPrices,), {'__bind_key__': vendor})


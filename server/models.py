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

    serialize_rules = ('-canonical_product.products', '-supplier.products')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    canonical_product_id = db.Column(db.Integer, db.ForeignKey('canonical_products.id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    supplier_sku = db.Column(db.String, nullable=False)
    image_link = db.Column(db.String)
    price_preset = db.Column(db.Float)

    # Relationships #
    canonical_product = db.relationship('CanonicalProduct', back_populates='products')
    supplier = db.relationship('Supplier', back_populates='products')

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

    serialize_only = ('id', 'manufacturer_id', 'manufacturer_sku', 'name', 
                      'description', 'image_link', 'price_preset', 'products.id', 
                      'products.supplier.name', 'products.supplier_sku', 
                      'suppliers.id', 'suppliers.name', 'manufacturer.id', 
                      'manufacturer.name')
    id = db.Column(db.Integer, primary_key=True)
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturers.id'))
    manufacturer_sku = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    image_link = db.Column(db.String)

    # 'Core price' for product. Suppliers will charge a markup on this price, and also randomly vary price by practice.
    price_preset = db.Column(db.Float)

    # Relationships #
    products = db.relationship('Product', back_populates='canonical_product')
    manufacturer = db.relationship('Manufacturer', back_populates='canonical_products')
    suppliers = association_proxy('products', 'supplier')

    # Validations #
    # -- Manufacturer SKUs must be unique for each manufacturer
    # @validates('manufacturer_sku')
    # def validate_manufacturer_sku(self, key, manufacturer_sku):
    #     assert not CanonicalProduct.query.filter_by(manufacturer_id=self.manufacturer_id, manufacturer_sku=manufacturer_sku).first()
    #     return manufacturer_sku


class Manufacturer(db.Model, SerializerMixin):
    __tablename__ = 'manufacturers'

    serialize_rules = ('-canonical_products.manufacturer', '-products.manufacturer')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    # Relationships #
    canonical_products = db.relationship('CanonicalProduct', back_populates='manufacturer')
    products = association_proxy('canonical_products', 'products')

class Supplier(db.Model, SerializerMixin):
    __tablename__ = 'suppliers'

    serialize_rules = ('-products.supplier', '-supplier_accounts.supplier', '-vendor_orders.supplier')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    house_brand = db.Column(db.String, nullable=False)
    preferred = db.Column(db.Boolean, nullable=False)

    # # Relationships
    products = db.relationship('Product', back_populates='supplier')
    supplier_accounts = db.relationship('SupplierAccount', back_populates='supplier')
    vendor_orders = db.relationship('VendorOrder', back_populates='supplier')

class SupplierAccount(db.Model, SerializerMixin):
    __tablename__ = 'supplier_accounts'

    # serialize_rules = ('-supplier.supplier_accounts', '-practice.supplier_accounts')
    serialize_only = ('id', 'supplier_id', 'practice_id', 'username', 'password', 'valid', 'last_validated', 'created_time', 'supplier.name', 'supplier.id', 'practice.name', 'practice.id')

    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    practice_id = db.Column(db.Integer, db.ForeignKey('practices.id'))
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    valid = db.Column(db.Boolean, nullable=False)
    last_validated = db.Column(db.DateTime)
    created_time = db.Column(db.DateTime, nullable=False)

    # # Relationships #
    supplier = db.relationship('Supplier', back_populates='supplier_accounts')
    practice = db.relationship('Practice', back_populates='supplier_accounts')

    # # Potential Validations #
    # # -- Only one account is allowed for each supplier/practice pair
    
    
class Practice(db.Model, SerializerMixin):
    __tablename__ = 'practices'

    serialize_only = ('id', 'name', 'created_time')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    created_time = db.Column(db.DateTime, nullable=False)

    # # Relationships #
    supplier_accounts = db.relationship('SupplierAccount', back_populates='practice')
    suppliers = association_proxy('supplier_accounts', 'supplier')
    users = db.relationship('User', back_populates='practice')
    addresses = db.relationship('Address', back_populates='practice')
    orders = db.relationship('Order', back_populates='practice')
    payment_methods = db.relationship('PaymentMethod', back_populates='practice')
    

class Address(db.Model, SerializerMixin):
    __tablename__ = 'addresses'

    serialize_only = ('id', 'practice_id', 'line_1', 'line_2', 'city', 'us_state', 'zip_code', 'is_primary_shipping')

    id = db.Column(db.Integer, primary_key=True)
    practice_id = db.Column(db.Integer, db.ForeignKey('practices.id'))
    line_1 = db.Column(db.String, nullable=False)
    line_2 = db.Column(db.String)
    city = db.Column(db.String, nullable=False)
    us_state = db.Column(db.String, nullable=False)
    zip_code = db.Column(db.String, nullable=False)
    is_primary_shipping = db.Column(db.Boolean, nullable=False)

    # # Relationships #
    practice = db.relationship('Practice', back_populates='addresses')
    orders = db.relationship('Order', back_populates='shipping_address')

    # # Validations #

    # # Only one primary shipping address is allowed for each practice #
    # @validates('is_primary_shipping')
    # def validate_is_primary_shipping(self, key, is_primary_shipping):
    #     if is_primary_shipping:
    #         assert not Address.query.filter_by(practice_id=self.practice_id, is_primary_shipping=True).first()
    #     return is_primary_shipping
    
    

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-practice', '-orders')

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String)
    practice_id = db.Column(db.Integer, db.ForeignKey('practices.id'))
    role = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    is_primary = db.Column(db.Boolean, nullable=False)

    # # Relationships #
    practice = db.relationship('Practice', back_populates='users')
    orders = db.relationship('Order', back_populates='placed_by_user')

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

    # serialize_rules = ('-practice', '-placed_by_user', '-payment_method', '-shipping_addresses', '-order_items', '-vendor_orders')
    serialize_only = ('id', 'practice_id', 'placed_by_user_id', 
                      'created_time', 'placed_time', 'status', 
                      'payment_method_id', 'shipping_address_id', 
                      'placed_by_user.id', 'placed_by_user.first_name', 
                      'placed_by_user.last_name', 'shipping_address.id',
                      'shipping_address.line_1', 'shipping_address.line_2',
                      'shipping_address.city', 'shipping_address.us_state',
                      'shipping_address.zip_code')

    id = db.Column(db.Integer, primary_key=True)
    practice_id = db.Column(db.Integer, db.ForeignKey('practices.id'))
    placed_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_time = db.Column(db.DateTime, nullable=False)
    placed_time = db.Column(db.DateTime)
    status = db.Column(db.String, nullable=False)
    payment_method_id = db.Column(db.Integer, db.ForeignKey('payment_methods.id'))
    shipping_address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'))

    # # Relationships #
    practice = db.relationship('Practice', back_populates='orders')
    placed_by_user = db.relationship('User', foreign_keys=[placed_by_user_id], post_update=True)
    payment_method = db.relationship('PaymentMethod', back_populates='orders')
    shipping_address = db.relationship('Address', back_populates='orders')
    order_items = db.relationship('OrderItem', back_populates='order')
    vendor_orders = db.relationship('VendorOrder', back_populates='order')

    # Validations #
    # Status can be 'in_cart', 'placed', 'delivered'
class OrderItem(db.Model, SerializerMixin):
    __tablename__ = 'order_items'

    serialize_only = ('id', 'order_id', 'fulfilled_by_product_id', 
                      'created_time', 'canonical_product_id', 
                      'canonical_product.name', 
                      'canonical_product.manufacturer.name', 
                      'quantity', 'price', 'vendor_order_id', 
                      'fulfilled_by_product.id', 
                      'fulfilled_by_product.supplier.name', 
                      'fulfilled_by_product.supplier_sku')

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    fulfilled_by_product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    created_time = db.Column(db.DateTime, nullable=False)
    canonical_product_id = db.Column(db.Integer, db.ForeignKey('canonical_products.id'))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float)
    vendor_order_id = db.Column(db.Integer, db.ForeignKey('vendor_orders.id'))
    cancelled = db.Column(db.Boolean)

    # # Relationships #
    order = db.relationship('Order', back_populates='order_items')
    fulfilled_by_product = db.relationship('Product', foreign_keys=[fulfilled_by_product_id], post_update=True)
    canonical_product = db.relationship('CanonicalProduct', foreign_keys=[canonical_product_id], post_update=True)
    vendor_order = db.relationship('VendorOrder', back_populates='order_items')



class VendorOrder(db.Model, SerializerMixin):
    __tablename__ = 'vendor_orders'

    serialize_only = ('id', 'order_id', 'supplier_id', 
                      'shipping_and_handling', 'tax',
                      'tracking_number', 'estimated_delivery_date',
                      'order.practice_id', 'order.placed_by_user_id',
                      'supplier.name', 'supplier.id',
                      'order_items.id', 'order_items.fulfilled_by_product_id', 
                      'order_items.fulfilled_by_product.name')
    

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    shipping_and_handling = db.Column(db.Float)
    tax = db.Column(db.Float, nullable=False)
    tracking_number = db.Column(db.String)
    estimated_delivery_date = db.Column(db.DateTime)

    # # Relationships #
    order = db.relationship('Order', back_populates='vendor_orders')
    order_items = db.relationship('OrderItem', back_populates='vendor_order')
    supplier = db.relationship('Supplier', back_populates='vendor_orders')

class PaymentMethod(db.Model, SerializerMixin):
    __tablename__ = 'payment_methods'

    id = db.Column(db.Integer, primary_key=True)
    practice_id = db.Column(db.Integer, db.ForeignKey('practices.id'))
    billing_address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'))
    nickname = db.Column(db.String)
    is_primary = db.Column(db.Boolean)

    # # Relationships #
    orders = db.relationship('Order', back_populates='payment_method')
    practice = db.relationship('Practice', back_populates='payment_methods')
    billing_address = db.relationship('Address', foreign_keys=[billing_address_id], post_update=True)


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
    free_shipping_threshold = db.Column(db.Float)
    shipping_cost = db.Column(db.Float)

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


from flask import Flask, jsonify, request, session, make_response
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restful import Api, Resource 
from flask_cors import CORS
import os
from dotenv import load_dotenv
from models import db, User, Product, CanonicalProduct, Order, Practice, OrderItem, SupplierAccount, Supplier
import models
from datetime import datetime
from random import randint, choice, randrange
import itertools

# ----- ENVIRONMENT VARIABLES ----- #
load_dotenv()
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

# ----- FLASK SETUP ----- #
app = Flask(__name__)

# Ensure integrity of session data
app.secret_key = FLASK_SECRET_KEY

# Set default db to app.db & create binds for other dbs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_BINDS'] = {
    'heartysoupsinternational': 'sqlite:///heartysoupsinternational.db',
    'planterson': 'sqlite:///planterson.db',
    'lentsplysproutona': 'sqlite:///lentsplysproutona.db',
    'lentilcity': 'sqlite:///lentilcity.db',
    'dclentil': 'sqlite:///dclentil.db',
}

# 'False' to avoid overhead of tracking all CRUD updates
# I may want to change this later to keep detailed logs
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set SameSite to Lax to avoid warnings in Chrome
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Keep JSON responses human-readable
app.json.compact = False

# Safely encrypt passwords
bcrypt = Bcrypt(app)

# Handle database migrations
migrate = Migrate(app, db)
db.init_app(app)

# So the browser doesn't complain about CORS
CORS(app)
# This is a more specific way to do it, but I'm not 100% sure what it does
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


# ----- API SETUP ----- #

# We may eventually want a v2 -- so, this is v1!
URL_PREFIX = '/api/v1'
api = Api(app, prefix=URL_PREFIX)

class Home(Resource):
    def get(self):
        return {"message": "Serving data and lentil soup..."}, 200
api.add_resource(Home, '/')

# ----- AUTHORIZATION ----- #
class CheckSession(Resource):
    def get(self):
        print("Route CHECKSESSION ...")
        if 'user_id' in session:
            user = User.query.filter_by(id=session['user_id']).first()
            response = {'user': user.to_dict()}, 200
            print("Response:", response)
            return response
        else:
            response = {'message': 'No user logged in'}, 401
            print("Response:", response)
            return response
api.add_resource(CheckSession, '/checksession')

# curl requests for testing:
# curl -i -X POST -H "Content-Type: application/json" -d '{"email":"ppadilla@example.net","password":"password"}' http://localhost:5555/api/v1/login
class Login(Resource):
    def post(self):
        print("Route LOGIN ...")
        data = request.json
        print("Data:", data)
        user = User.query.filter_by(email=data['email']).first()
        print("User:", user)
        if user is None:
            return {'message': 'Invalid email'}, 401
        if bcrypt.check_password_hash(user.password, data['password']):
            session['user_id'] = user.id
            return {'user': user.to_dict()}, 200
        else:
            return {'message': 'Incorrect password'}, 401
api.add_resource(Login, '/login')

class Logout(Resource):
    def delete(self):
        print("Route LOGOUT ...")
        session.clear()
        response = {'message': 'Session cleared'}, 200
        print(response)
        return response
api.add_resource(Logout, '/logout')

# curl requests for testing:
# curl -i -X POST -H "Content-Type: application/json" -d '{"email":"halliesala@example.com","password":"password","first_name":"Hallie","last_name":"Sala"}' http://localhost:5555/api/v1/apply
class Apply(Resource):
    def post(self):
        print("Route APPLY ...")
        data = request.json
        user = User.query.filter_by(email=data['email']).first()
        if user is not None:
            response = {'message': 'Email already taken'}, 401
            print("Response: ", response)
            return response
        else:
            try:
                new_admin = User(
                    email = data['email'],
                    password = bcrypt.generate_password_hash(data['password']).decode('utf-8'),
                    practice_id = None,
                    role='admin',
                    first_name = data['first_name'],
                    last_name = data['last_name'],
                    is_primary = False,
                )
                db.session.add(new_admin)
                db.session.commit()
                session['user_id'] = new_admin.id
                response = new_admin.to_dict(), 200
                print("Response: ", response)
                return response
            except:
                response = {'message': 'Missing form fields'}, 401
                print("Response: ", response)
                return response
    def patch(self):
        data = request.json
        user = User.query.filter_by(id=session['user_id']).first() 
        user.role = data['role']
        db.session.commit()
        response = user.to_dict(), 200
        print("Response: ", response)
        return response        
api.add_resource(Apply, '/apply')

# curl requests for testing:
# curl -i -X POST -H "Content-Type: application/json" -d '{"practice_name":"My Example Practice","email": "example@example.com", "password":"password", "first_name":"John", "last_name":"Doe"}' http://localhost:5555/api/v1/signup
class Signup(Resource):
    def post(self):
        print("Route APPLY ...")
        data = request.json
        practice = Practice.query.filter_by(id=data['practice_name']).first()
        user = User.query.filter_by(email=data['email']).first()
        if practice is not None:
            response = {'message': 'Practice name already taken.'}, 401
            print("Response: ", response)
            return response
        elif user is not None:
            response = {'message': 'Email already taken'}, 401
            print("Response: ", response)
            return response
        else:
            new_practice = Practice(
                name=data['practice_name'],
                created_time = datetime.now(),
            )
            db.session.add(new_practice)
            db.session.commit()
            new_user = User(
                email = data['email'],
                password = bcrypt.generate_password_hash(data['password']).decode('utf-8'),
                practice_id = new_practice.id,
                role='lentist',
                first_name = data['first_name'],
                last_name = data['last_name'],
                is_primary = True,
            )
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            response = new_user.to_dict(), 200
        print("Response: ", response)
        return response
api.add_resource(Signup, '/signup')

# ----- SHOP ---- #
class Products(Resource):
    def get(self):
        products = Product.query.all()
        return [p.to_dict() for p in products], 200
api.add_resource(Products, '/products')

class CanonicalProducts(Resource):
    def get(self):
        canonical_products = CanonicalProduct.query.all()
        return [cp.to_dict() for cp in canonical_products], 200
api.add_resource(CanonicalProducts, '/canonical_products')

class PracticeOrders(Resource):
    def get(self, practice_id):
        orders = Order.query.filter_by(practice_id=practice_id).all()
        return [o.to_dict() for o in orders], 200
api.add_resource(PracticeOrders, '/practice=<int:practice_id>/orders')

class Practices(Resource):
    def get(self, id):
        practice = Practice.query.filter_by(id=id).first()
        return practice.to_dict(), 200
api.add_resource(Practices, '/practice=<int:id>')

class Orders(Resource):
    def get(self):
        orders = Order.query.all()
        return [o.to_dict() for o in orders], 200
api.add_resource(Orders, '/orders')

class Suppliers(Resource):
    def get(self):
        return [s.to_dict() for s in Supplier.query.all()], 200
api.add_resource(Suppliers, '/suppliers')

# ----- CART ----- #
class OrderItemsByOrderID(Resource):
    def get(self, order_id):
        order_items = OrderItem.query.filter_by(order_id=order_id).all()
        return [oi.to_dict() for oi in order_items], 200
api.add_resource(OrderItemsByOrderID, '/order=<int:order_id>/items')

class OrderItemByID(Resource):
    def patch(self, id):
        print("Route ORDERITEM ...")
        print("Updating order item ...")
        data = request.json
        order_item = OrderItem.query.filter_by(id=id).first()
        if not order_item:
            response = {'message': 'Order item not found'}, 401
            print("Response: ", response)
            return response
        order_item.quantity = data['quantity']
        db.session.commit()
        response = order_item.to_dict(), 200
        print("Response: ", response)
        return response
    
    def delete(self, id):
        print("Route ORDERITEM ...")
        print("Deleting order item ...")
        order_item = OrderItem.query.filter_by(id=id).first()
        if not order_item:
            response = {'message': 'Order item not found'}, 401
            print("Response: ", response)
            return response
        db.session.delete(order_item)
        db.session.commit()
        # 204 'no content'
        response = {'message': 'Order item deleted'}, 204
api.add_resource(OrderItemByID, '/orderitem=<int:id>')

class Cart(Resource):
    # curl -i -X GET http://localhost:5555/api/v1/cart
    def get(self):
        print("Route CART ...")
        print("Getting cart ...")
        if 'user_id' not in session:
            response = {'message': 'No user logged in'}, 401
            print("Response: ", response)
            return response
        user = User.query.filter_by(id=session['user_id']).first()
        if user.practice_id is None:
            response = {'message': "User must belong to a practice"}, 401
            print("Response: ", response)
            return response
        # Get active order
        active_cart = Order.query.filter_by(practice_id=user.practice_id, status='in_cart').first()
        if not active_cart:
            # Create new order
            active_cart = Order(
                practice_id = user.practice_id,
                created_time = datetime.now(),
                status = 'in_cart',
            )
            db.session.add(active_cart)
            db.session.commit()
        order_items = OrderItem.query.filter_by(order_id=active_cart.id).all()
        response = {'order': active_cart.to_dict(), 'order_items': [oi.to_dict() for oi in order_items]}, 200
        print("Response: ", response)
        return response

    # curl -i -X POST -H "Content-Type: application/json" -d '{"user_id":1,"canonical_product_id":1,"quantity":1}' http://localhost:5555/api/v1/additemtocart
    def post(self):
        print("Route CART ...")
        print("Adding item to cart ...")
        data = request.json
        # data should contain user_id, canonical_product_id, and quantity
        if not 'user_id' in data and 'canonical_product_id' in data and 'quantity' in data:
            response = {'message': "Request must contain user_id, canonical_product_id, and quantity"}, 401
            print("Response: ", response)
            return response
        # Check if user belongs to a practice
        user = User.query.filter_by(id=data['user_id']).first()
        if user.practice_id is None:
            response = {'message': "User must belong to a practice"}, 401
            print("Response: ", response)
            return response
        # Get active order
        active_cart = Order.query.filter_by(practice_id=user.practice_id, status='in_cart').first()
        if not active_cart:
            # Create new order
            active_cart = Order(
                practice_id = user.practice_id,
                created_time = datetime.now(),
                status = 'in_cart',
            )
            db.session.add(active_cart)
            db.session.commit()
        # Check if item already exists in cart
        existing_item = OrderItem.query.filter_by(order_id=active_cart.id, canonical_product_id=data['canonical_product_id']).first()
        if existing_item:
            existing_item.quantity += data['quantity']
            db.session.commit()
            response = existing_item.to_dict(), 200
            print("Response: ", response)
            return response
        else:
            new_item = OrderItem(
                order_id = active_cart.id,
                canonical_product_id = data['canonical_product_id'],
                quantity = data['quantity'],
                created_time = datetime.now(),
            )
            db.session.add(new_item)
            db.session.commit()
            response = new_item.to_dict(), 200
            print("Response: ", response)
            return response
api.add_resource(Cart, '/cart')


class OptimizeCart(Resource):
    # Get user, practice, cart
    def get(self):
        print("Route OPTIMIZECART ...")

        # Return error if no user logged in or user doesn't belong to practice
        user = User.query.filter_by(id=session['user_id']).first()
        if user is None:
            response = {'message': 'No user logged in'}, 401
            print("Response: ", response)
            return response
        practice = user.practice
        if practice is None:
            response = {'message': "User must belong to a practice"}, 401
            print("Response: ", response)
            return response
        active_cart = Order.query.filter_by(practice_id=practice.id, status='in_cart').first()

        # Get order items and prices
        order_items = OrderItem.query.filter_by(order_id=active_cart.id).all()
        prices = {oi.id: getAllProductPriceInfo(oi.canonical_product_id, user.practice_id) for oi in order_items}

        # Check all possible cart combinations to find lowest overall price
        possible_fulfillments = {oi.id: [p.id for p in oi.canonical_product.products] 
                                 for oi in order_items}
        possible_carts = []
        for possible_cart in itertools.product(*possible_fulfillments.values()):
            possible_carts.append(possible_cart)


        
        # for oi in order_items:
        #     print("Checking order item: ", oi.id)
        #     for (vendor_name, product_info) in prices[oi.id].items():
        #         print("Vendor:", vendor_name)
        #         print("Product info:", product_info)

        
        

        return {'user': user.to_dict(), 
                'practice': practice.to_dict(), 
                'cart': active_cart.to_dict(), 
                'order_items': [oi.to_dict() for oi in order_items], 
                'prices': prices}, 200

api.add_resource(OptimizeCart, '/optimizecart')


# ----- PRICES ----- #
# Gets practice-specific price for a supplier product
def getPriceInfo(product_id, practice_id):
    # print("Calling function getPriceInfo ...")

    product = models.Product.query.filter_by(id=product_id).first()
    supplier = product.supplier
    # print("SUPPLIER: ", supplier.name, supplier.id)
    
    supplier_account = models.SupplierAccount.query.filter_by(practice_id=practice_id, supplier_id=supplier.id).first()
    # print("SUPPLIER ACCOUNT: ", supplier_account)
    if not supplier_account:
        return {
            'message': "practice is missing this supplier",
            'product_id': product_id,
            'supplier_sku': product.supplier_sku,
        }

    vendor_prefix = f"{product.supplier.name.replace(' ', '').capitalize()}"
    
    vendor_product_class = getattr(models, f"{vendor_prefix}Product")
    vendor_product = vendor_product_class.query.filter_by(sku=product.supplier_sku).first()
    
    vendor_user_class= getattr(models, f"{vendor_prefix}User")
    
    
    vendor_user = vendor_user_class.query.filter_by(username=supplier_account.username, password=supplier_account.password).first()
    
    return {
        'product_id': product_id,
        'supplier_sku': product.supplier_sku,
        'preset': vendor_product.price_preset, 
        'multiplier': vendor_user.price_multiplier, 
        'price': vendor_product.price_preset * vendor_user.price_multiplier,
        'stock': vendor_product.stock, # num items in stock
        'days_to_ship': vendor_user.days_to_ship, 
        'free_shipping_threshold': vendor_user.free_shipping_threshold, 
        'shipping_cost': vendor_user.shipping_cost
    }
# Gets practice-specific prices for all supplier products in a canonical product
def getAllProductPriceInfo(cp_id, practice_id):
    # print("Calling function getAllProductPriceInfo ...")
    products = models.Product.query.filter_by(canonical_product_id=cp_id).all()
    info = {p.supplier.name: getPriceInfo(p.id, practice_id) for p in products}
    return info
# curl -i -X GET http://localhost:5555/api/v1/getpriceinfo/cp=1/practice=14
class GetPriceInfo(Resource):
    def get(self, cp_id, practice_id):
        print("Route GETPRICEINFO ...")
        return getAllProductPriceInfo(cp_id, practice_id), 200
api.add_resource(GetPriceInfo, '/getpriceinfo/cp=<int:cp_id>/practice=<int:practice_id>')


class GetCartPrices(Resource):
    def get(self):
        if 'user_id' not in session:
            response = {'message': 'No user logged in'}, 401
            print("Response: ", response)
            return response
        user = User.query.filter_by(id=session['user_id']).first()
        if user.practice_id is None:
            response = {'message': "User must belong to a practice"}, 401
            print("Response: ", response)
            return response
        # Get active order
        active_cart = Order.query.filter_by(practice_id=user.practice_id, status='in_cart').first()
        if not active_cart:
            # Create new order
            active_cart = Order(
                practice_id = user.practice_id,
                created_time = datetime.now(),
                status = 'in_cart',
            )
            db.session.add(active_cart)
            db.session.commit()
        order_items = OrderItem.query.filter_by(order_id=active_cart.id).all()
        prices = {oi.id: getAllProductPriceInfo(oi.canonical_product_id, user.practice_id) for oi in order_items}
        return prices, 200
api.add_resource(GetCartPrices, '/getcartprices')
          
class SupplierAccountsByID(Resource):
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if user.practice_id is None:
            response = {'message': "User must belong to a practice"}, 401
            print("Response: ", response)
            return response
        supplier_accounts = SupplierAccount.query.filter_by(practice_id=user.practice_id).all()
        return [sa.to_dict() for sa in supplier_accounts], 200
api.add_resource(SupplierAccountsByID, '/supplieraccounts/user=<int:user_id>')

class SupplierAccounts(Resource):
    def get(self):
        if 'user_id' not in session:
            response = {'message': 'No user logged in'}, 401
            print("Response: ", response)
            return response
        user = User.query.filter_by(id=session['user_id']).first()
        if user.practice_id is None:
            response = {'message': "User must belong to a practice"}, 401
            print("Response: ", response)
            return response
        supplier_accounts = SupplierAccount.query.filter_by(practice_id=user.practice_id).all()
        return [sa.to_dict() for sa in supplier_accounts], 200
api.add_resource(SupplierAccounts, '/supplieraccounts')
        
class ConnectVendor(Resource):
    def post(self):
        data = request.json
        vendor_id = data['vendor_id']
        username = data['username']
        password = data['password']
        # Get user from session
        user = User.query.filter_by(id=session['user_id']).first()
        supplier = Supplier.query.filter_by(id=vendor_id).first()
        # Get practice from user
        # If no practice, return error
        if user.practice_id is None:
            response = {'message': 'User must belong to a practice'}, 401
            print("Response: ", response)
            return response
        # If practice, look for existing supplier account
        supplier_account = SupplierAccount.query.filter_by(practice_id=user.practice.id, supplier_id=vendor_id).first()
        # If existing supplier account, return error
        if supplier_account:
            response = {'message': 'Supplier account already exists'}, 401
            print("Response: ", response)
            return response
        # If no existing supplier account, create new supplier account 
        # & corresponding VendorUser record
        supplier_account = SupplierAccount(
            practice_id = user.practice.id,
            supplier_id = vendor_id,
            username = username,
            password = password,
            valid = True,
            last_validated = datetime.now(),
            created_time = datetime.now(),
        )
        vendor_prefix = f"{supplier.name.replace(' ', '').capitalize()}"
        vendor_user_class= getattr(models, f"{vendor_prefix}User")
        # Preferred vendors vs non-preferred
        price_multiplier = 1.0 if supplier.preferred else randrange(80, 120) / 100
        shipping_cost = 9.99 if supplier.preferred else choice([9.99, 14.99, 19.99])
        free_shipping_threshold = 49.99 if supplier.preferred else choice([0, 49.99, 99.99, 199.99])
        
        vendor_user = vendor_user_class(
            username=username,
            password=password,
            price_multiplier = price_multiplier,
            days_to_ship = randint(1, 5),
            free_shipping_threshold = free_shipping_threshold,
            shipping_cost = shipping_cost,
        )

        db.session.add(supplier_account)
        db.session.add(vendor_user)

        db.session.commit()
        # Return account
        response = {'supplier_account': supplier_account.to_dict(), 'VendorUser record': vendor_user.to_dict()}, 200
        print("Response: ", response)
        return response
api.add_resource(ConnectVendor, '/connectvendor')

# Server will run on port 5555
if __name__ == "__main__":
    app.run(port=5555)
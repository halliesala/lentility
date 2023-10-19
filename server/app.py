from flask import Flask, jsonify, request, session, make_response
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restful import Api, Resource 
from flask_cors import CORS
import os
from dotenv import load_dotenv
from models import (db, User, Product, CanonicalProduct, Order, 
                    Practice, OrderItem, SupplierAccount, Supplier, 
                    Address, PaymentMethod, VendorOrder)
import models
from datetime import datetime, timedelta
from random import randint, choice, randrange
import itertools
import pprint

pp = pprint.PrettyPrinter(indent=4)

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


class OrdersByLoggedInPractice(Resource):
    def get(self):
        print("Route ORDERSBYLOGGEDINPRACTICE ...")
        print("Getting orders ...")
        if 'user_id' not in session:
            response = {'message': 'No user logged in'}, 401
            print("Response: ", response)
            return response
        user = User.query.filter_by(id=session['user_id']).first()
        if user.practice_id is None:
            response = {'message': "User must belong to a practice"}, 401
            print("Response: ", response)
            return response
        orders = Order.query.filter_by(practice_id=user.practice_id).all()
        return [o.to_dict() for o in orders if o.status != 'in_cart'], 200
api.add_resource(OrdersByLoggedInPractice, '/ordersbyloggedinpractice')


class AddressesByLoggedInPractice(Resource):
    def get(self):
        print("Route ADDRESSESBYLOGGEDINPRACTICE ...")
        print("Getting addresses ...")
        if 'user_id' not in session:
            response = {'message': 'No user logged in'}, 401
            print("Response: ", response)
            return response
        user = User.query.filter_by(id=session['user_id']).first()
        if user.practice_id is None:
            response = {'message': "User must belong to a practice"}, 401
            print("Response: ", response)
            return response
        addresses = Address.query.filter_by(practice_id=user.practice_id).all()
        return [a.to_dict() for a in addresses], 200
api.add_resource(AddressesByLoggedInPractice, '/addressesbyloggedinpractice')

# curl -i -X POST -H "Content-Type: application/json" -d '{"shipping_address_id": 2}' http://localhost:5555/api/v1/addshippingaddress
class UpdatePrimaryShippingAddress(Resource):
    def post(self):
        print("Route UPDATESHIPPINGADDRESS ...")
        # Contains shipping_address_id
        data = request.json
        # Get user, practice, and all shipping addresses
        if 'user_id' not in session:
            response = {'message': 'No user logged in'}, 401
            print("Response: ", response)
            return response
        user = User.query.filter_by(id=session['user_id']).first()
        if user.practice_id is None:
            response = {'message': "User must belong to a practice"}, 401
            print("Response: ", response)
            return response
        addresses = Address.query.filter_by(practice_id=user.practice_id).all()
        # Set new primary and confirm no others are set to primary
        for a in addresses:
            if a.id == data['address_id']:
                a.is_primary_shipping = True
            else:
                a.is_primary_shipping = False
        db.session.commit()
        response = [a.to_dict() for a in addresses], 200
        print(response)
        return response
api.add_resource(UpdatePrimaryShippingAddress, '/updateprimaryshippingaddress')

class PaymentMethodsByLoggedInPractice(Resource):
    def get(self):
        print("Route PAYMENTMETHODSBYLOGGEDINPRACTICE ...")
        print("Getting payment methods ...")
        if 'user_id' not in session:
            response = {'message': 'No user logged in'}, 401
            print("Response: ", response)
            return response
        user = User.query.filter_by(id=session['user_id']).first()
        if user.practice_id is None:
            response = {'message': "User must belong to a practice"}, 401
            print("Response: ", response)
            return response
        payment_methods = PaymentMethod.query.filter_by(practice_id=user.practice_id).all()
        return [pm.to_dict() for pm in payment_methods], 200
api.add_resource(PaymentMethodsByLoggedInPractice, '/paymentmethodsbyloggedinpractice')

class Suppliers(Resource):
    def get(self):
        return [s.to_dict() for s in Supplier.query.all()], 200
api.add_resource(Suppliers, '/suppliers')

class VendorOrdersByOrderID(Resource):
    def get(self, order_id):
        vendor_orders = VendorOrder.query.filter_by(order_id=order_id).all()
        return [vo.to_dict() for vo in vendor_orders], 200
api.add_resource(VendorOrdersByOrderID, '/order=<int:order_id>/vendororders')

class OrderItemByVendorOrderID(Resource):
    def get(self, vendor_order_id):
        order_items = OrderItem.query.filter_by(vendor_order_id=vendor_order_id).all()
        return [oi.to_dict() for oi in order_items], 200
api.add_resource(OrderItemByVendorOrderID, '/vendororder=<int:vendor_order_id>/items')

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



# ----- PRICES AND CART OPTIMIZATION----- #

# ----- HELPER FUNCTIONS ----- #
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
# Optimizes cart by total price
def getOptimizedByPrice(user_id):

    user = models.User.query.filter_by(id=user_id).first()

    practice_id = user.practice_id
    order_id = models.Order.query.filter_by(practice_id=practice_id, status='in_cart').first().id
    
    # Get cart -- #89  is Thursday Test Practice's active cart
    cart = models.Order.query.filter_by(id=order_id).first()

    # Get prices for all products in cart 
    fulfillment_options = {}
    for item in cart.order_items:
        fulfillment_options[item.id] = getAllProductPriceInfo(item.canonical_product_id, practice_id=practice_id)

    connected_fulfillments = {}
    # Get all combinations of product fulfillments
    for (order_item_id, options) in fulfillment_options.items():
        for (vendor_name, product_info) in options.items():
            if 'price' in product_info:
                connected_fulfillments[order_item_id] = connected_fulfillments.get(order_item_id, []) + [product_info['product_id']]


    # Get Cartesian product of all fulfillments
    all_fulfillments = list(itertools.product(*connected_fulfillments.values()))
    # print(all_fulfillments)

    # For each possible fulfillment, calculate total price
    fulfillment_prices = []
    fulfillment_prices_dict = {}
    for fulfillment in all_fulfillments:
        total = 0
        subtotal = 0
        shipping = 0
        vendor_subtotals = {}
        vendor_free_shipping_thresholds = {}
        vendor_shipping_below_threshold = {}
        vendor_shipping = {}
        for product_id in fulfillment:
            product = models.Product.query.filter_by(id=product_id).first()
            supplier = product.supplier
            price_info = getPriceInfo(product_id, practice_id=practice_id)
            subtotal += price_info['price']
            vendor_subtotals[supplier.name] = vendor_subtotals.get(supplier.name, 0) + price_info['price']
            vendor_shipping_below_threshold[supplier.name] = price_info['shipping_cost']
            vendor_free_shipping_thresholds[supplier.name] = price_info['free_shipping_threshold']
        for (vendor, subtotal) in vendor_subtotals.items():
            # calculate shipping cost
            if subtotal < vendor_free_shipping_thresholds[vendor]:
                vendor_shipping[vendor] = vendor_shipping_below_threshold[vendor]
                shipping += vendor_shipping[vendor]
        total = subtotal + shipping
        fulfillment_prices.append((fulfillment, total, subtotal, shipping, vendor_subtotals, vendor_shipping_below_threshold))
        fulfillment_prices_dict[fulfillment] = {'total': total, 'subtotal': subtotal, 'shipping': shipping, 'vendor_subtotals': vendor_subtotals, 'vendor_shipping_below_threshold': vendor_shipping_below_threshold, 'vendor_free_shipping_thresholds': vendor_free_shipping_thresholds}
    fulfillment_prices.sort(key=lambda x: x[1])
    
    # For now, 'best' fulfillment is the one with the lowest total price
    best_fulfillment = min(fulfillment_prices_dict, key=lambda x: fulfillment_prices_dict[x]['total'])
    print("Best fulfillment:", best_fulfillment)

    order_item_to_fulfilled_product_map = {}
    for product_id in best_fulfillment:
        product = models.Product.query.filter_by(id=product_id).first()
        order_item = models.OrderItem.query.filter_by(order_id=order_id, canonical_product_id=product.canonical_product_id).first()
        order_item_to_fulfilled_product_map[order_item.id] = product_id

    return {'order_item_to_fulfilled_product_map': order_item_to_fulfilled_product_map, 'info': fulfillment_prices_dict[best_fulfillment]}

# ----- API ENDPOINTS ----- #
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

class OptimizeCart(Resource):
    # Get optimization info without fulfilling order items
    def get(self):
        print("Route OPTIMIZECART (GET) ...")

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
        order_items = OrderItem.query.filter_by(order_id=active_cart.id).all()
    

        best_fulfillment_info = getOptimizedByPrice(user.id)
        return {'user': user.to_dict(), 
                'practice': practice.to_dict(), 
                'cart': active_cart.to_dict(), 
                'order_items': [oi.to_dict() for oi in order_items], 
                'best_fulfillment_info': best_fulfillment_info}, 200
    # Fulfill order items
    # curl -i -X POST -H "Content-Type: application/json" -d '{}' http://localhost:5555/api/v1/optimizecart
    def post(self):
        print("Route OPTIMIZECART (POST) ...")
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
        order_items = OrderItem.query.filter_by(order_id=active_cart.id).all()
        best_fulfillment_info = getOptimizedByPrice(user.id)
        for oi in order_items:
            try:
                fulfilled_by_product_id = best_fulfillment_info['order_item_to_fulfilled_product_map'][oi.id]
                oi.fulfilled_by_product_id = fulfilled_by_product_id
                oi.price = getPriceInfo(fulfilled_by_product_id, practice.id)['price']
            except:
                # No connected vendor can fulfill this item; it will need to be cancelled
                pass
        db.session.commit()
        response = {'order_items': [oi.to_dict() for oi in order_items], 'best_fulfillment_info': best_fulfillment_info}, 200
        pp.pprint(response)

        return response
api.add_resource(OptimizeCart, '/optimizecart')

# curl -i -X POST -H "Content-Type: application/json" -d '{"shipping_address_id":1,"payment_method_id":1}' http://localhost:5555/api/v1/placeorder
class PlaceOrder(Resource):
    def post(self):
        # Contains shipping_address_id, payment_method_id
        data = request.json
        # Get user -> practice -> cart
        # Optimize cart
        print("Route PLACEORDER ...")
        # Return error if no user logged in or user doesn't belong to practice
        # user = User.query.filter_by(id=session['user_id']).first()
        user = User.query.filter_by(id=1).first()
        if user is None:
            response = {'message': 'No user logged in'}, 401
            print("Response: ", response)
            return response
        practice = user.practice
        if practice is None:
            response = {'message': "User must belong to a practice"}, 401
            print("Response: ", response)
            return response
        orders = Order.query.filter_by(practice_id=practice.id).all()
        print("ORDERS: ", [(o.id, o.status) for o in orders])
        active_cart = Order.query.filter_by(practice_id=practice.id, status='in_cart').first()
        print("ACTIVE CART: ", active_cart)
        order_items = OrderItem.query.filter_by(order_id=active_cart.id).all()
        print("Optimizing price ... (this may take a while) ...")
        best_fulfillment_info = getOptimizedByPrice(user.id)
        print("Optimization complete.")
        print("Best fulfillment info:", best_fulfillment_info)
        for oi in order_items:
            try:
                fulfilled_by_product_id = best_fulfillment_info['order_item_to_fulfilled_product_map'][oi.id]
                oi.fulfilled_by_product_id = fulfilled_by_product_id
                oi.price = getPriceInfo(fulfilled_by_product_id, practice.id)['price']
            except:
                # No connected vendor can fulfill this item; it will need to be cancelled
                oi.cancelled = True
        db.session.commit()
        # Patch Order shipping_address_id, payment_method_id, placed_by_user, placed_time, and status
        print("Updating order ...")
        active_cart.shipping_address_id = data['shipping_address_id']
        active_cart.payment_method_id = data['payment_method_id']
        active_cart.placed_by_user_id = user.id
        active_cart.placed_time = datetime.now()
        active_cart.status = 'placed'
        db.session.commit()
        
        # Post VendorOrders
        print("Creating vendor orders ...")
        vendor_orders = []
        vendor_subtotals = best_fulfillment_info['info']['vendor_subtotals']
        vendor_ids = [oi.fulfilled_by_product.supplier_id for oi in order_items if oi.fulfilled_by_product]
        print(vendor_ids)
        vendor_ids = list(set(vendor_ids))
        for vendor_id in vendor_ids:
            vendor = Supplier.query.filter_by(id=vendor_id).first()
            items = [oi for oi in order_items if not oi.cancelled and oi.fulfilled_by_product.supplier_id == vendor_id]
            free_shipping_threshold = best_fulfillment_info['info']['vendor_free_shipping_thresholds'][vendor.name]
            shipping_cost_below_threshold = best_fulfillment_info['info']['vendor_shipping_below_threshold'][vendor.name]
            subtotal = best_fulfillment_info['info']['vendor_subtotals'][vendor.name]
            shipping = shipping_cost_below_threshold if subtotal < free_shipping_threshold else 0
            vendor_order = VendorOrder(
                order_id = active_cart.id,
                supplier_id = vendor_id,
                shipping_and_handling = shipping,
                tax = 0.07 * subtotal,
                tracking_number = '1Z' + str(randint(1000000000, 9999999999)),
                estimated_delivery_date = datetime.now() + timedelta(days=5),
            )
            db.session.add(vendor_order)
            db.session.commit()
            for item in items:
                item.vendor_order_id = vendor_order.id
            vendor_orders.append(vendor_order)
        db.session.add_all(vendor_orders)
        db.session.commit()
        # Return success message
        response = {'message': 'Order placed successfully', 
                    'vendor_orders': [vo.to_dict() for vo in vendor_orders],
                    'order': active_cart.to_dict(),
                    'order_items': [oi.to_dict() for oi in order_items]}, 200
        pp.pprint(response)
        return response
api.add_resource(PlaceOrder, '/placeorder')


# ----- SUPPLIER ACCOUNTS AND CONNECT VENDOR ----- #

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
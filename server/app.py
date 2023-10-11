from flask import Flask, jsonify, request, session, make_response
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restful import Api, Resource 
from flask_cors import CORS
import os
from dotenv import load_dotenv
from models import db, User, Product, CanonicalProduct, Order, Practice, OrderItem
from datetime import datetime

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
        return {'message': 'Session cleared'}, 200
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

# ----- CART ----- #
class OrderItemsByOrderID(Resource):
    def get(self, order_id):
        order_items = OrderItem.query.filter_by(order_id=order_id).all()
        return [oi.to_dict() for oi in order_items], 200
api.add_resource(OrderItemsByOrderID, '/order=<int:order_id>/items')

class OrderItemByID(Resource):
    def patch(self, id):
        print("Route ORDERITEM ...")
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
        response = [oi.to_dict() for oi in order_items], 200
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
    pass
api.add_resource(OptimizeCart, '/optimizecart')

# Server will run on port 5555
if __name__ == "__main__":
    app.run(port=5555)
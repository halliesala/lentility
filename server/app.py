from flask import Flask, jsonify, request, session, make_response
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restful import Api, Resource 
from flask_cors import CORS
import os
from dotenv import load_dotenv
from models import db, User, Product, CanonicalProduct, Order, Practice

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
        print("Checking session...")
        if 'user_id' in session:
            user = User.query.filter_by(id=session['user_id']).first()
            print('USER: ', user)
            return {'user': user.to_dict()}, 200
        else:
            return {'message': 'No user logged in'}, 401
api.add_resource(CheckSession, '/checksession')

# curl requests for testing:
# curl -i -X POST -H "Content-Type: application/json" -d '{"email":"ppadilla@example.net","password":"password"}' http://localhost:5555/api/v1/login
class Login(Resource):
    def post(self):
        data = request.json
        user = User.query.filter_by(email=data['email']).first()
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
        session.clear()
        return {'message': 'Session cleared'}, 200
api.add_resource(Logout, '/logout')

# curl requests for testing:
# curl -i -X POST -H "Content-Type: application/json" -d '{"email":"halliesala@example.com","password":"password","first_name":"Hallie","last_name":"Sala"}' http://localhost:5555/api/v1/apply
class Apply(Resource):
    def post(self):
        data = request.json
        user = User.query.filter_by(email=data['email']).first()
        if user is not None:
            return {'message': 'Email already taken'}, 401
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
                return new_admin.to_dict(), 200
            except:
                return {'message': 'Missing form fields'}, 401
    def patch(self):
        data = request.json
        user = User.query.filter_by(email=data['email']).first() 
        user.role = 'admin'
        db.session.commit()
        return user.to_dict(), 200       
    
api.add_resource(Apply, '/apply')

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


# Add route to get all orders for all practices
class Orders(Resource):
    def get(self):
        orders = Order.query.all()
        return [o.to_dict() for o in orders], 200
api.add_resource(Orders, '/orders')

# Server will run on port 5555
if __name__ == "__main__":
    app.run(port=5555)
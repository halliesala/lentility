from flask import Flask, jsonify, request, session
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restful import Api, Resource 
from flask_cors import CORS
import os
from dotenv import load_dotenv
from models import db, User

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

# curl requests for testing:
# curl -i -X POST -H "Content-Type: application/json" -d '{"email":"ppadilla","password":"password"}' http://localhost:5555/api/v1/chec
class CheckSession(Resource):
    def get(self):
        print("Checking session...")
        if 'user_id' in session:
            user = User.query.filter_by(id=session['user_id']).first()
            print('USER: ', user)
            return {'user': user.to_dict()}, 200
        else:
            return {'error': 'No user logged in'}, 401
api.add_resource(CheckSession, '/checksession')

# curl requests for testing:
# curl -i -X POST -H "Content-Type: application/json" -d '{"email":"ppadilla@example.net","password":"password"}' http://localhost:5555/api/v1/login
class Login(Resource):
    def post(self):
        print('Login request received...')
        data = request.json
        print('DATA: ', data)

        user = User.query.filter_by(email=data['email']).first()
        if user is None:
            return {'error': 'Invalid email'}, 401
        print('USER: ', user)
        if bcrypt.check_password_hash(user.password, data['password']):
            session['user_id'] = user.id
            return {'user': user.to_dict()}, 200
        else:
            return {'error': 'Incorrect password'}, 401
api.add_resource(Login, '/login')



# Server will run on port 5555
if __name__ == "__main__":
    app.run(port=5555)
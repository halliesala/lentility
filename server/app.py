from flask import Flask, jsonify, request, session
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt


from models import db

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'

# Set default db to app.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'

# 
app.config['SQLALCHEMY_BINDS'] = {
    'heartysoupsinternational': 'sqlite:///heartysoupsinternational.db',
    'planterson': 'sqlite:///planterson.db',
    'lentsplysproutona': 'sqlite:///lentsplysproutona.db',
    'housebrand1': 'sqlite:///housebrand1.db',
    'housebrand2': 'sqlite:///housebrand2.db',
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

bcrypt = Bcrypt(app)

migrate = Migrate(app, db)

db.init_app(app)

URL_PREFIX = '/api/v1'


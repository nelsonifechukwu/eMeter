from flask import Flask
from flask_cors import CORS
from app.config import Config

app = Flask(__name__)
CORS(app, resources={r"/plot/*": {"origins": "http://127.0.0.1:5000"}})
#set the app configuration from an object
app.config.from_object(Config)

from app import routes

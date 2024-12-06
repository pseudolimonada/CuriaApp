from flask import Flask, request, jsonify
from flask_cors import CORS
from db_models import *
import json
from config import Config
from extensions import db
from db_setup import init_db

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes

app.config.from_object(Config)
db.init_app(app)  # Initialize the db instance with the app
init_db()
print("Backend at http://127.0.0.1:5000/")


@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Hello, World!"}), 200


if __name__ == "__main__":
    app.run(debug=True)

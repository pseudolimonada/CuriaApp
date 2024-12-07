from flask import Flask, request, jsonify
from flask_cors import CORS
from db_models import *
from config import Config, APP_PORT, APP_URL
from extensions import db
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from constants import hash_password

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes

app.config.from_object(Config)
db.init_app(app)  # Initialize the db instance with the app
with app.app_context():
    db.create_all()
    print("Tables created")
print(f"Backend at {APP_URL}:{APP_PORT}/")

ENDPOINT_TO_BE_IMPLEMENTED = (jsonify({ "error": "TO BE IMPLEMETED" }), 501)

@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Hello, World!"}), 200


@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.__dict__ for user in users]), 200


@app.route("/users", methods=["POST"])
def register_or_login_user():
    assert request.json is not None, "Request Json is None"

    user_data = {
        "user_name": request.json.get("user_name"),
        "password": request.json.get("password"),
    }

    user = User.query.filter_by(
        user_name=user_data["user_name"], password=hash_password(user_data["password"])
    ).first()

    if user:
        # TODO: generate JWT token with user_id
        return jsonify(user.user_id), 200

    business_id = request.json.get("business_id", None)
    if business_id:
        business = Business.query.filter_by(business_id=business_id).first()
        if not business:
            return jsonify({"error": "Business not found"}), 404

    try:
        with db.session.begin():
            user = User(**user_data)
            db.session.add(user)
            db.session.flush()

            if business_id:
                business_user = BusinessUser(user_id=user.id, business_id=business_id)
                db.session.add(business_user)

            db.session.commit()
        return jsonify(user.user_id), 201
    except IntegrityError as e:
        db.session.rollback()
        if isinstance(e.orig, UniqueViolation):
            return jsonify({"error": "User already exists"}), 400
        return jsonify({"error": str(e.orig)}), 400
    except Exception as e:
        breakpoint()
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route('/register', methods=["POST"])
def register():
    return ENDPOINT_TO_BE_IMPLEMENTED


@app.route("/businesses", methods=["GET"])
def get_businesses():
    businesses = Business.query.all()
    return jsonify([business.__dict__ for business in businesses]), 200


@app.route("/businesses", methods=["POST"])
def create_business():
    assert request.json is not None, "Request Json is None"

    business_data = {
        "business_name": request.json.get("business_name"),
    }
    try:
        with db.session.begin():
            business = Business(**business_data)
            db.session.add(business)
            db.session.commit()
        return jsonify(business.business_id), 201
    except IntegrityError as e:
        db.session.rollback()
        if isinstance(e.orig, UniqueViolation):
            return jsonify({"error": "Business already exists"}), 400
        return jsonify({"error": str(e.orig)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


# TODO: create a wrapper that checks the JWT header
# @validate_business_user
@app.route("/businesses/<int:business_id>", methods=["GET"])
def create_order():
    assert request.json is not None, "Request Json is None"

    return ENDPOINT_TO_BE_IMPLEMENTED

@app.route('/businesses/<int:business_id>/orders', methods=['POST'])
def submit_order():
    assert request.json is not None, "Request Json is None"

    return ENDPOINT_TO_BE_IMPLEMENTED

@app.route('/businesses/<int:business_id>/products', methods=['GET'])
def get_products():
    assert request.json is not None, "Request Json is None"

    return ENDPOINT_TO_BE_IMPLEMENTED

@app.route('/businesses/<int:business_id>/products', methods=['POST'])
def post_product():
    assert request.json is not None, "Request Json is None"

    return ENDPOINT_TO_BE_IMPLEMENTED

@app.route('/businesses/<int:business_id>/products/<int:product_id>', methods=['PUT'])
def put_product():
    assert request.json is not None, "Request Json is None"

    return ENDPOINT_TO_BE_IMPLEMENTED

@app.route('/businesses/<int:business_id>/catalogs', methods=['GET'])
def get_catalogs():
    assert request.json is not None, "Request Json is None"

    return ENDPOINT_TO_BE_IMPLEMENTED

@app.route('/businesses/<int:business_id>/catalogs', methods=['POST'])
def post_catalogs():
    assert request.json is not None, "Request Json is None"

    return ENDPOINT_TO_BE_IMPLEMENTED

@app.route('/businesses/<int:business_id>/orders', methods=['GET'])
def get_orders():
    assert request.json is not None, "Request Json is None"

    return ENDPOINT_TO_BE_IMPLEMENTED



if __name__ == "__main__":
    app.run(debug=True, port=APP_PORT)

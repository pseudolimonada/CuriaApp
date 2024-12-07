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

ENDPOINT_TO_BE_IMPLEMENTED = (jsonify({"error": "TO BE IMPLEMENTED"}), 501)

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
        return jsonify({"user_id": user.user_id}), 200

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
        return jsonify({"user_id": user.user_id}), 201
    except IntegrityError as e:
        db.session.rollback()
        if isinstance(e.orig, UniqueViolation):
            return jsonify({"error": "User already exists"}), 400
        return jsonify({"error": str(e.orig)}), 400
    except Exception as e:
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
        return jsonify({"business_id": business.business_id}), 201
    except IntegrityError as e:
        db.session.rollback()
        if isinstance(e.orig, UniqueViolation):
            return jsonify({"error": "Business already exists"}), 400
        return jsonify({"error": str(e.orig)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@app.route("/businesses/<int:business_id>", methods=["GET"])
def get_business(business_id):
    business = Business.query.get(business_id)
    if business:
        return jsonify(business.__dict__), 200
    else:
        return jsonify({"error": "Business not found"}), 404


@app.route('/businesses/<int:business_id>/orders', methods=['POST'])
def submit_order():
    assert request.json is not None, "Request Json is None"

    order_data = {
        "user_id": request.json.get("user_id"),
        "order_date": request.json.get("order_date"),
        "order_data": request.json.get("order_data"),
    }

    try:
        with db.session.begin():
            order = Order(**order_data, business_id=business_id)
            db.session.add(order)
            db.session.commit()
        return jsonify({"order_id": order.order_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@app.route('/businesses/<int:business_id>/products', methods=['GET'])
def get_products(business_id):
    products = Product.query.filter_by(business_id=business_id).all()
    return jsonify([product.__dict__ for product in products]), 200


@app.route('/businesses/<int:business_id>/products', methods=['POST'])
def post_product(business_id):
    assert request.json is not None, "Request Json is None"

    product_data = {
        "business_id": business_id,
        "image_url": request.json.get("image_url"),
        "product_title": request.json.get("product_title"),
        "product_description": request.json.get("product_description"),
        "product_price": request.json.get("product_price"),
    }

    try:
        with db.session.begin():
            product = Product(**product_data)
            db.session.add(product)
            db.session.commit()
        return jsonify({"product_id": product.product_id}), 201
    except IntegrityError as e:
        db.session.rollback()
        if isinstance(e.orig, UniqueViolation):
            return jsonify({"error": "Product already exists"}), 400
        return jsonify({"error": str(e.orig)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@app.route('/businesses/<int:business_id>/products/<int:product_id>', methods=['PUT'])
def put_product(business_id, product_id):
    assert request.json is not None, "Request Json is None"

    product = Product.query.get(product_id)
    if not product or product.business_id != business_id:
        return jsonify({"error": "Product not found"}), 404

    if "image_url" in request.json:
        product.image_url = request.json["image_url"]
    if "product_title" in request.json:
        product.product_title = request.json["product_title"]
    if "product_description" in request.json:
        product.product_description = request.json["product_description"]
    if "product_price" in request.json:
        product.product_price = request.json["product_price"]

    db.session.commit()
    return jsonify({"message": "Product updated successfully"}), 200


@app.route('/businesses/<int:business_id>/catalogs', methods=['GET'])
def get_catalogs(business_id):
    catalogs = Catalog.query.filter_by(business_id=business_id).all()
    return jsonify([catalog.__dict__ for catalog in catalogs]), 200


@app.route('/businesses/<int:business_id>/catalogs', methods=['POST'])
def post_catalogs(business_id):
    assert request.json is not None, "Request Json is None"

    return ENDPOINT_TO_BE_IMPLEMENTED


@app.route('/businesses/<int:business_id>/orders', methods=['GET'])
def get_orders(business_id):
    # Assuming that we can confirm the user identity based on JWT
    orders = Order.query.filter_by(business_id=business_id).all()
    return jsonify([order.__dict__ for order in orders]), 200


if __name__ == "__main__":
    app.run(debug=True, port=APP_PORT)

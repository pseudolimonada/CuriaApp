from flask import Blueprint, request, jsonify
from db_models import Product
from extensions import db
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

products_blueprint = Blueprint('products', __name__)

@products_blueprint.route("/", methods=["GET"])
def get_products(business_id):
    products = Product.query.filter_by(business_id=business_id).all()
    return jsonify([product.__dict__ for product in products]), 200

@products_blueprint.route("/", methods=["POST"])
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

@products_blueprint.route("/<int:product_id>", methods=['PUT'])
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

from flask import Blueprint, request, jsonify
from db_models import Product
from extensions import db
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from constants import jwt_required

products_blueprint = Blueprint("products", __name__)


@products_blueprint.route("/<int:business_id>/products", methods=["GET"])
@jwt_required()
def get_products(business_id):
    products = Product.query.filter_by(business_id=business_id).all()
    catalog = {}
    for product in products:
        catalog[product.product_id] = {
            "product_name": product.product_name,
            "product_description": product.product_description,
            "product_price": product.product_price,
            "image_url": product.image_url,
        }
    return jsonify({"catalog": catalog}), 200


@products_blueprint.route("/<int:business_id>/products", methods=["POST"])
@jwt_required(admin_required=True)
def post_product(business_id):
    assert request.json is not None, "Request Json is None"

    product_data = {
        "business_id": business_id,
        "image_url": request.json.get("image_url"),
        "product_name": request.json.get("product_name"),
        "product_description": request.json.get("product_description"),
        "product_price": request.json.get("product_price"),
    }

    try:
        product = Product(**product_data)
        db.session.add(product)
        db.session.commit()
        return get_products(business_id)
    except IntegrityError as e:
        db.session.rollback()
        if isinstance(e.orig, UniqueViolation):
            return jsonify({"error": "Product already exists"}), 400
        return jsonify({"error": str(e.orig)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@products_blueprint.route(
    "/<int:business_id>/products/<int:product_id>", methods=["PUT"]
)
@jwt_required(admin_required=True)
def put_product(business_id, product_id):
    assert request.json is not None, "Request Json is None"

    product = Product.query.get(product_id)
    if not product or product.business_id != business_id:
        return jsonify({"error": "Product not found"}), 404

    if "image_url" in request.json:
        product.image_url = request.json["image_url"]
    if "product_name" in request.json:
        product.product_name = request.json["product_name"]
    if "product_description" in request.json:
        product.product_description = request.json["product_description"]
    if "product_price" in request.json:
        product.product_price = request.json["product_price"]

    db.session.commit()
    return get_products(business_id)


@products_blueprint.route(
    "/<int:business_id>/products/<int:product_id>", methods=["DELETE"]
)
@jwt_required(admin_required=True)
def delete_product(business_id, product_id):
    product = Product.query.get(product_id)
    if not product or product.business_id != business_id:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()
    return get_products(business_id)

from flask import Blueprint, request, jsonify
from db_models import Order
from extensions import db

orders_blueprint = Blueprint('orders', __name__)

@orders_blueprint.route("/", methods=["GET"])
def get_orders(business_id):
    orders = Order.query.filter_by(business_id=business_id).all()
    return jsonify([order.__dict__ for order in orders]), 200

@orders_blueprint.route("/", methods=["POST"])
def submit_order(business_id):
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

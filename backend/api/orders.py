from flask import Blueprint, request, jsonify
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db_models import Order
from extensions import db
from  notification_new_order.notification_new_order import notification_new_order

orders_blueprint = Blueprint('orders', __name__)
print(orders_blueprint)
@orders_blueprint.route("/", methods=["GET"])
def get_orders(business_id):
    orders = Order.query.filter_by(business_id=business_id).all()
    print = ([order.__dict__ for order in orders])
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
            asyncio.create_task(notify_new_order(business_id, order_data))            
        return jsonify({"order_id": order.order_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

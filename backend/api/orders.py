from flask import Blueprint, request, jsonify, g
from db_models import Order, OrderProduct, CatalogProduct, Catalog
from extensions import db
from constants import jwt_required, OrderStateType, serialize_date

orders_blueprint = Blueprint("orders", __name__)


@orders_blueprint.route("/<int:business_id>/orders", methods=["GET"])
@jwt_required()
def get_orders(business_id):
    try:
        if g.is_admin:
            orders = Order.query.filter_by(business_id=business_id).all()
        else:
            orders = Order.query.filter_by(
                business_id=business_id, user_id=g.user_id
            ).all()

        order_list = []
        for order in orders:
            order_products = OrderProduct.query.filter_by(order_id=order.order_id).all()
            order_product_list = []
            order_list.append(
                {
                    "order_id": str(order.order_id),
                    "order_date": serialize_date(order.order_date),
                    "order_state": OrderStateType(order.order_state).value,
                    "order_data": [
                        {
                            "product_id": str(order_product.product_id),
                            "product_quantity": order_product.product_quantity,
                        }
                        for order_product in order_products
                    ],
                }
            )

        return jsonify({"orders": order_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@orders_blueprint.route("/<int:business_id>/orders", methods=["POST"])
@jwt_required()
def submit_order(business_id):
    if not request.json:
        return jsonify({"error": "Request Json is None"}), 400

    order_object_data = {
        "user_id": g.user_id,
        "order_date": request.json.get("order_date"),
        "order_state": OrderStateType.TO_BE_VALIDATED,
        "business_id": business_id,
    }

    try:
        order = Order(**order_object_data)
        db.session.add(order)
        db.session.flush()

        catalog = Catalog.query.filter_by(
            business_id=business_id, catalog_date=request.json.get("order_date")
        ).first()

        if not catalog:
            db.session.rollback()
            return jsonify({"error": "Catalog not found"}), 404

        for product in request.json.get("order_data"):
            catalog_product = CatalogProduct.query.filter_by(
                catalog_id=catalog.catalog_id, product_id=product.get("product_id")
            ).first()

            if not catalog_product:
                db.session.rollback()
                return jsonify({"error": "Product not found in catalog"}), 404

            if (
                catalog_product.product_quantity_sold + product.get("product_quantity")
                > catalog_product.product_quantity_total
            ):
                db.session.rollback(),
                return (
                    jsonify({"error": "Product quantity exceeds catalog quantity"}),
                    400,
                )

            order_product = OrderProduct(
                order_id=order.order_id,
                product_id=product.get("product_id"),
                product_quantity=product.get("product_quantity"),
            )
            db.session.add(order_product)
            catalog_product.product_quantity_sold += product.get("product_quantity")

        db.session.commit()
        return jsonify({"order_id": order.order_id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@orders_blueprint.route("/<int:business_id>/orders/<int:order_id>", methods=["PUT"])
@jwt_required()
def change_order_state(business_id, order_id):
    if not request.json:
        return jsonify({"error": "Request Json is None"}), 400

    try:
        order_state = OrderStateType(value=request.json.get("order_state"))
        order = Order.query.get(order_id)
        if not order or order.business_id != business_id:
            return jsonify({"error": "Order not found"}), 404

        delete_from_catalog = False

        if order.order_state == OrderStateType.TO_BE_VALIDATED:
            if order_state == OrderStateType.REJECTED:
                delete_from_catalog = True
            elif order_state != OrderStateType.TO_BE_DELIVERED:
                return jsonify({"error": "Invalid order state"}), 400

        elif order.order_state == OrderStateType.TO_BE_DELIVERED:
            if order_state == OrderStateType.REJECTED:
                delete_from_catalog = True
            elif order_state != OrderStateType.DELIVERED:
                return jsonify({"error": "Invalid order state"}), 400

        elif order.order_state == OrderStateType.DELIVERED:
            return jsonify({"error": "Invalid order state"}), 400

        order.order_state = order_state
        update_catalog(business_id, order, rejected=delete_from_catalog)
        result, code = get_orders(business_id)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    return result, code


def update_catalog(business_id, order, sold=False, rejected=False):
    if not sold and not rejected:
        return
    try:
        catalog = Catalog.query.filter_by(
            business_id=business_id, catalog_date=order.order_date
        ).first()
        order_products = OrderProduct.query.filter_by(order_id=order.order_id).all()
        for order_product in order_products:
            catalog_product = CatalogProduct.query.filter_by(
                catalog_id=catalog.catalog_id, product_id=order_product.product_id
            ).first()
            if sold:
                catalog_product.product_quantity_sold += order_product.product_quantity
            elif rejected:
                catalog_product.product_quantity_sold -= order_product.product_quantity
    except Exception as e:
        raise Exception(f"Error updating catalog: {str(e)}")

from flask import Blueprint, request, jsonify, g
from db_models import Catalog, CatalogProduct, Business, Product
from extensions import db
from constants import jwt_required, validate_date

orders_blueprint = Blueprint("orders", __name__)


@orders_blueprint.route("/<int:business_id>/catalogs", methods=["GET"])
@jwt_required
def get_week_catalogs(business_id):
    # get monday_date from query param
    monday_start_date = validate_date(request.args.get("monday_date"))

    # get catalogs starting at monday_date adn ending 7 days later
    catalogs = (
        Catalog.query.filter(
            Catalog.business_id == business_id,
            Catalog.catalog_date >= monday_start_date,
            Catalog.catalog_date < monday_start_date + 7,
        )
        .order_by(Catalog.catalog_date)
        .all()
    )

    catalog = {
        "Mon": CatalogProduct.query.filter_by(catalog_id=catalogs[0].catalog_id).all(),
        "Tue": CatalogProduct.query.filter_by(catalog_id=catalogs[1].catalog_id).all(),
        "Wed": CatalogProduct.query.filter_by(catalog_id=catalogs[2].catalog_id).all(),
        "Thu": CatalogProduct.query.filter_by(catalog_id=catalogs[3].catalog_id).all(),
        "Fri": CatalogProduct.query.filter_by(catalog_id=catalogs[4].catalog_id).all(),
        "Sat": CatalogProduct.query.filter_by(catalog_id=catalogs[5].catalog_id).all(),
        "Sun": CatalogProduct.query.filter_by(catalog_id=catalogs[6].catalog_id).all(),
    }

    for day in catalog:
        if g.is_admin:
            catalog[day] = [
                {
                    "product_id": product.product_id,
                    "product_quantity_total": product.product_quantity_total,
                    "product_quantity_sold": product.product_quantity_sold,
                }
                for product in catalog[day]
            ]
        else:
            catalog[day] = [
                {
                    "product_id": product.product_id,
                    "product_scarcity": (
                        product.product_quantity_total - product.product_quantity_sold
                        if product.product_quantity_total
                        - product.product_quantity_sold
                        < 5
                        else None
                    ),
                }
                for product in catalog[day]
            ]

    return jsonify(catalog), 200


@orders_blueprint.route("/<int:business_id>/catalogs", methods=["POST"])
@jwt_required
def submit_catalog(business_id):
    assert request.json is not None, "Request Json is None"

    catalog_date = request.json.get("catalog_date")
    catalog_products = request.json.get("catalog_products")

    try:
        with db.session.begin():
            catalog = Catalog(business_id=business_id, catalog_date=catalog_date)
            db.session.add(catalog)
            db.session.flush()

            for product in request.json.get("products"):
                catalog_product = CatalogProduct(
                    catalog_id=catalog.catalog_id,
                    product_id=product.get("product_id"),
                    product_quantity_total=product.get("product_quantity_total"),
                )
                db.session.add(catalog_product)

            db.session.commit()
        return jsonify({"catalog_id": catalog.catalog_id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

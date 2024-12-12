from flask import Blueprint, request, jsonify, g
from db_models import Catalog, CatalogProduct, Business, Product
from extensions import db
from constants import jwt_required, validate_date
from datetime import timedelta

catalog_blueprint = Blueprint("catalog", __name__)


@catalog_blueprint.route("/<int:business_id>/catalogs", methods=["GET"])
@jwt_required()
def get_week_catalogs(business_id, monday_date=None):
    # get monday_date from query param
    try:
        monday_date = (
            validate_date(request.args.get("monday_date"))
            if not monday_date
            else monday_date
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    # get catalogs starting at monday_date adn ending 7 days later
    catalogs = [
        Catalog.query.filter(
            Catalog.business_id == business_id, Catalog.catalog_date == monday_date
        ).first(),
        Catalog.query.filter(
            Catalog.business_id == business_id,
            Catalog.catalog_date == monday_date + timedelta(days=1),
        ).first(),
        Catalog.query.filter(
            Catalog.business_id == business_id,
            Catalog.catalog_date == monday_date + timedelta(days=2),
        ).first(),
        Catalog.query.filter(
            Catalog.business_id == business_id,
            Catalog.catalog_date == monday_date + timedelta(days=3),
        ).first(),
        Catalog.query.filter(
            Catalog.business_id == business_id,
            Catalog.catalog_date == monday_date + timedelta(days=4),
        ).first(),
        Catalog.query.filter(
            Catalog.business_id == business_id,
            Catalog.catalog_date == monday_date + timedelta(days=5),
        ).first(),
        Catalog.query.filter(
            Catalog.business_id == business_id,
            Catalog.catalog_date == monday_date + timedelta(days=6),
        ).first(),
    ]

    product_catalog = {}
    product_catalog["Mon"] = (
        CatalogProduct.query.filter_by(catalog_id=catalogs[0].catalog_id).all()
        if catalogs[0]
        else []
    )
    product_catalog["Tue"] = (
        CatalogProduct.query.filter_by(catalog_id=catalogs[1].catalog_id).all()
        if catalogs[1]
        else []
    )
    product_catalog["Wed"] = (
        CatalogProduct.query.filter_by(catalog_id=catalogs[2].catalog_id).all()
        if catalogs[2]
        else []
    )
    product_catalog["Thu"] = (
        CatalogProduct.query.filter_by(catalog_id=catalogs[3].catalog_id).all()
        if catalogs[3]
        else []
    )
    product_catalog["Fri"] = (
        CatalogProduct.query.filter_by(catalog_id=catalogs[4].catalog_id).all()
        if catalogs[4]
        else []
    )
    product_catalog["Sat"] = (
        CatalogProduct.query.filter_by(catalog_id=catalogs[5].catalog_id).all()
        if catalogs[5]
        else []
    )
    product_catalog["Sun"] = (
        CatalogProduct.query.filter_by(catalog_id=catalogs[6].catalog_id).all()
        if catalogs[6]
        else []
    )

    new_product_catalog = {}
    for day in product_catalog:
        if g.is_admin:
            new_product_catalog[day] = {}
            for product in product_catalog[day]:
                new_product_catalog[day][str(product.product_id)] = {
                    "product_quantity_total": product.product_quantity_total,
                    "product_quantity_sold": product.product_quantity_sold,
                }
        else:
            new_product_catalog[day] = {}
            for product in product_catalog[day]:
                new_product_catalog[day][str(product.product_id)] = {
                    # "product_quantity_total": product.product_quantity_total,
                    "product_scarcity": (
                        product.product_quantity_total - product.product_quantity_sold
                        if (
                            product.product_quantity_total
                            - product.product_quantity_sold
                        )
                        <= 5
                        else None
                    )
                }

    return jsonify(new_product_catalog), 200


@catalog_blueprint.route("/<int:business_id>/catalogs", methods=["POST"])
@jwt_required()
def submit_catalog(business_id):
    assert request.json is not None, "Request Json is None"

    catalog_date = validate_date(request.json.get("catalog_date"))
    catalog_products = request.json.get("catalog_products")

    try:
        catalog = Catalog(business_id=business_id, catalog_date=catalog_date)
        db.session.add(catalog)
        db.session.flush()
        db_catalog_products = CatalogProduct.query.filter_by(
            catalog_id=catalog.catalog_id
        ).all()

        # delete all products from catalog
        for product in db_catalog_products:
            if str(product.product_id) in catalog_products:
                catalog_products[str(product.product_id)][
                    "product_quantity_sold"
                ] = product.product_quantity_sold
            db.session.delete(product)
        db.session.flush()

        for product_id, product in catalog_products.items():
            db_product = Product.query.get(int(product_id))

            if not db_product or db_product.business_id != business_id:
                db.session.rollback()
                return jsonify({"error": "Product not found"}), 400

            catalog_product = CatalogProduct(
                catalog_id=catalog.catalog_id,
                product_id=int(product_id),
                product_quantity_total=product["product_quantity_total"],
                product_quantity_sold=product.get("product_quantity_sold", 0),
            )
            db.session.add(catalog_product)

        # get updated catalog
        db.session.flush()

        # get the monday date before the catalog date if it is not a monday
        monday_date = catalog.catalog_date - timedelta(
            days=catalog.catalog_date.weekday()
        )
        result, code = get_week_catalogs(business_id, monday_date=monday_date)
        db.session.commit()

        return result, code
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

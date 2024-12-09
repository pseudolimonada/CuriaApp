from flask import Blueprint, request, jsonify
from db_models import Business
from extensions import db
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

businesses_blueprint = Blueprint('businesses', __name__)

@businesses_blueprint.route("/", methods=["GET"])
def get_businesses():
    businesses = Business.query.all()
    return jsonify([business.__dict__ for business in businesses]), 200

@businesses_blueprint.route("/", methods=["POST"])
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

from flask import Blueprint, request, jsonify
from db_models import Business
from extensions import db
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from constants import jwt_required

businesses_blueprint = Blueprint("businesses", __name__)


@businesses_blueprint.route("/", methods=["GET"])
@jwt_required()
def get_businesses():

    businesses = Business.query.all()
    if not businesses:
        return None

    business_list = []
    for business in businesses:
        business_dict = business.__dict__
        business_list.append(
            {
                "business_id": business_dict["business_id"],
                "business_name": business_dict["business_name"],
            }
        )
    return jsonify(business_list), 200


@businesses_blueprint.route("/", methods=["POST"])
@jwt_required()
def create_business():
    assert request.json is not None, "Request Json is None"

    business_data = {
        "business_name": request.json.get("business_name"),
    }
    try:
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

from flask import Blueprint, request, jsonify
from db_models import User, Business, BusinessUser
from extensions import db
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from constants import hash_password

users_blueprint = Blueprint('users', __name__)

@users_blueprint.route("/", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.__dict__ for user in users]), 200

@users_blueprint.route("/", methods=["POST"])
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
                business_user = BusinessUser(user_id=user.user_id, business_id=business_id)
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

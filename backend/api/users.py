from flask import Blueprint, request, jsonify, g
from db_models import User, Business, BusinessUser
from extensions import db
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from constants import hash_password, jwt_token, jwt_required, UserType, check_token


def build_token_data(user_id: int) -> dict:
    """
    Builds a list of businesses the user is associated with.

    :param user_id: User ID to search for.
    :return: List of businesses the user is associated with.
    """
    user = User.query.get(user_id)
    if not user:
        return None

    businesses = BusinessUser.query.filter_by(
        user_id=user_id, user_type=UserType.MANAGER
    ).all()

    return {
        "user_id": user_id,
        "manager_business_ids": [business.business_id for business in businesses],
    }


users_blueprint = Blueprint("users", __name__)


@users_blueprint.route("/", methods=["GET"])
@jwt_required(admin_required=True)
def get_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_dict = user.__dict__
        user_list.append(
            {"user_id": user_dict["user_id"], "user_name": user_dict["user_name"]}
        )
    return jsonify(user_list), 200


@users_blueprint.route("/register", methods=["POST"])
def register():
    business_id = request.json.get("business_id")
    if business_id:
        user_id, is_admin = check_token(request, business_id)
        if not is_admin or user_id != 1:
            return jsonify({"error": "Unauthorized"}), 401
        business = Business.query.filter_by(business_id=business_id).first()
        if not business:
            return jsonify({"error": "Business not found"}), 404

    try:
        user_data = {
            "user_name": request.json.get("user_name"),
            "password": request.json.get("password"),
        }
        user = User(
            user_name=user_data["user_name"],
            password=hash_password(user_data["password"]),
        )
        db.session.add(user)
        db.session.flush()

        if business_id:
            business_user = BusinessUser(
                user_id=user.user_id, business_id=business_id, user_type="MANAGER"
            )
            db.session.add(business_user)

        db.session.commit()
        return (
            jsonify({"token": jwt_token(build_token_data(user.user_id))}),
            201,
        )

    except IntegrityError as e:
        db.session.rollback()
        if isinstance(e.orig, UniqueViolation):
            return jsonify({"error": "User already exists"}), 400
        return jsonify({"error": str(e.orig)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@users_blueprint.route("/login", methods=["POST"])
def login():
    if not request.json:
        return jsonify({"error": "Request Json is None"}), 400

    user_name = request.json.get("user_name")
    password = request.json.get("password")

    if not user_name or not password:
        return jsonify({"error": "Missing user_name or password"}), 400

    user = User.query.filter_by(
        user_name=user_name, password=hash_password(password)
    ).first()
    if not user:
        return jsonify({"error": "Invalid user_name or password"}), 401

    return jsonify({"token": jwt_token(build_token_data(user.user_id))}), 200


@users_blueprint.route("/permissions/<int:business_id>", methods=["GET"])
@jwt_required()
def get_user_permissions(business_id):
    return {"is_admin": g.is_admin}, 200

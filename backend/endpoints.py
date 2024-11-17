import flask
from functools import wraps
import jwt
from psycopg2 import DatabaseError
from backend.api import token_required

STATUS_CODES = {"success": 200, "api_error": 400, "internal_error": 500}

app = flask.Flask(__name__)
# app.config["SECRET_KEY"] = config["APP_SECRET_KEY"]


@app.route("/users/validate", methods=["POST"])
def validate_user(username, password):
    pass


@app.route("/orders/<business_id>", methods=["POST"])
@token_required
def get_orders_by_date(business_id, **kwargs):
    user_id = kwargs.pop("user_id")
    user_type = user_id = kwargs.pop("user_type")

    pass

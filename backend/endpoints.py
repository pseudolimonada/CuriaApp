import flask
from functools import wraps
import jwt
from psycopg2 import DatabaseError
from backend.db.utils import check_user_against_db

STATUS_CODES = {"success": 200, "api_error": 400, "internal_error": 500}

app = flask.Flask(__name__)
# app.config["SECRET_KEY"] = config["APP_SECRET_KEY"]


# authorization decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "auth-token" in flask.request.headers:
            token = flask.request.headers["auth-token"]

        if not token:
            return flask.jsonify(
                {
                    "status": STATUS_CODES["api_error"],
                    "errors": "Authorization token is missing",
                }
            )

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])

            # check_user_against_db(flask.g.db_con, data['login_id'])
            kwargs["user_id"] = data["user_id"]
            kwargs["user_type"] = data["user_type"]

        except jwt.ExpiredSignatureError:
            return flask.jsonify(
                {
                    "status": STATUS_CODES["api_error"],
                    "errors": "Expired authorization token",
                }
            )
        except jwt.InvalidTokenError:
            return flask.jsonify(
                {
                    "status": STATUS_CODES["api_error"],
                    "errors": "Invalid authorization token",
                }
            )
        except Exception as e:
            return flask.jsonify(
                {"status": STATUS_CODES["internal_error"], "errors": str(e)}
            )

        return f(*args, **kwargs)

    return decorated


@app.route("/users/validate", methods=["POST"])
def validate_user(username, password):
    pass


@app.route("/orders/<business_id>", methods=["POST"])
@token_required
def get_orders_by_date(business_id, **kwargs):
    user_id = kwargs.pop("user_id")
    user_type = user_id = kwargs.pop("user_type")

    pass

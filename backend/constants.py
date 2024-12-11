from enum import Enum
from hashlib import sha256
from config import SECRET_KEY
import jwt
import datetime
import logging
from functools import wraps
from flask import request, jsonify

DB_MAX_ID_SIZE = 20
DB_MAX_EMAIL_SIZE = 320
DB_MAX_PWD_SIZE = 50


def hash_password(password: str) -> str:
    salted_password = password + SECRET_KEY
    return sha256(salted_password.encode()).hexdigest()


class WeekDay(Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


class UserType(Enum):
    USER = "user"
    MANAGER = "manager"


class OrderStateType(Enum):
    TO_BE_VALIDATED = "to_be_validated"
    TO_BE_DELIVERED = "to_be_delivered"
    REFUSED = "rejected"
    DELIVERED = "delivered"


def setup_logger() -> logging.Logger:
    # Create logger
    logger = logging.getLogger("logger")
    logger.setLevel(logging.DEBUG)

    # Create console handler and file handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    fh = logging.FileHandler("log_file.log", "a")
    fh.setLevel(logging.DEBUG)

    # Format handlers
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s]:  %(message)s", "%H:%M:%S"
    )
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # Add handlers
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger


LOGGER = setup_logger()


def jwt_token(data_to_encode: dict, expires_in: int = 360000) -> str:
    """
    Generates a JWT token from a dictionary.

    :param data_to_encode: Dictionary to encode in the JWT.
    :param expires_in: Expiration time in minutes.
    :return: Encoded JWT token as a string.
    """
    payload = data_to_encode.copy()
    payload["exp"] = datetime.datetime.now(
        tz=datetime.timezone.utc
    ) + datetime.timedelta(minutes=expires_in)

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def decode_jwt(token: str) -> dict:
    """
    Decodes a JWT token.

    :param token: JWT token to decode.
    :return: Decoded data as a dictionary.
    """
    try:
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_data
    except jwt.ExpiredSignatureError:
        LOGGER.error("Token has expired")
        raise
    except jwt.InvalidTokenError:
        LOGGER.error("Invalid token")
        raise


def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        try:
            decoded_data = decode_jwt(token)
            request.user_data = decoded_data
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs)

    return decorated_function

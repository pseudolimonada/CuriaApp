from enum import Enum
from hashlib import sha256
from config import SECRET_KEY
import logging

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


def jwt_token(data_to_encode: dict) -> str:
    pass

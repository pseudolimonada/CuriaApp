from enum import Enum
from hashlib import sha256
from config import SECRET_KEY

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

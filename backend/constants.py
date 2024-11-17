from enum import Enum

DB_MAX_ID_SIZE = 20
DB_MAX_EMAIL_SIZE = 320
DB_MAX_PWD_SIZE = 50


class UserType(Enum):
    USER = "user"
    MANAGER = "manager"


class OrderStateType(Enum):
    TO_BE_VALIDATED = "to_be_validated"
    TO_BE_DELIVERED = "to_be_delivered"
    DELIVERED = "delivered"

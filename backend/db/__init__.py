from db_classes import DBUser
from constants import (
    UserType,
    OrderStateType,
    DB_MAX_ID_SIZE,
    DB_MAX_EMAIL_SIZE,
    DB_MAX_PWD_SIZE,
)

SCHEMA = f"""
CREATE TYPE user_types AS ENUM ({','.join(f"'{i.value}'" for i in UserType
)});
CREATE TABLE IF NOT EXISTS "user" (
    "user_id" VARCHAR({DB_MAX_ID_SIZE}) NOT NULL PRIMARY KEY,
    "email" VARCHAR({DB_MAX_EMAIL_SIZE}) NOT NULL,
    "password" VARCHAR({DB_MAX_PWD_SIZE}) NOT NULL,
    "user_type" "user_types" NOT NULL
);

CREATE TYPE order_state_types AS ENUM ({','.join(f"'{i.value}'" for i in OrderStateType
)});
CREATE TABLE IF NOT EXISTS "order" (
    "order_id" VARCHAR({DB_MAX_ID_SIZE}) NOT NULL PRIMARY KEY,
    "created_date" TIMESTAMPTZ NOT NULL,
    "delivery_date" TIMESTAMPTZ NOT NULL,
    "state" "order_state_types" NOT NULL,
    "business_id" VARCHAR({DB_MAX_ID_SIZE}) NOT NULL
);

CREATE TABLE IF NOT EXISTS "order_unit" (
    "order_unit_id" VARCHAR({DB_MAX_ID_SIZE}) NOT NULL PRIMARY KEY,
    "order_class_id" VARCHAR({DB_MAX_ID_SIZE}) NOT NULL PRIMARY KEY,
    "order_id" VARCHAR({DB_MAX_ID_SIZE}) NOT NULL PRIMARY KEY,
    "quantity" VARCHAR({DB_MAX_PWD_SIZE}) NOT NULL,
);

CREATE TABLE IF NOT EXISTS "order_class" (
    "user_id" VARCHAR({DB_MAX_ID_SIZE}) NOT NULL PRIMARY KEY,
    "email" VARCHAR({DB_MAX_EMAIL_SIZE}) NOT NULL,
    "password" VARCHAR({DB_MAX_PWD_SIZE}) NOT NULL,
    "user_type" "user_types" NOT NULL
);

"""

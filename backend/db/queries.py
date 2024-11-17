from backend.db.utils import transactional, _build_insert_query
import hashlib
from backend.utils import logger


@transactional
def login_user(db_con, payload, cursor=None):
    # Query to check for username and password in the person table
    query = """
    SELECT user_id, user_type FROM user WHERE email = %s AND password = %s
    """
    print(payload["email"], payload["password"])
    values = (
        payload["username"],
        hashlib.sha256(payload["password"].encode()).hexdigest(),
    )

    cursor.execute(query, values)
    result = cursor.fetchone()

    if result is None:
        raise ValueError("Invalid username or password")

    user_id = result[0]

    return user_id


@transactional
def check_user_from_token(db_con, user_id, user_type=None, cursor=None):
    query = """
    SELECT user_id FROM user WHERE user_id = %s and user_type = %s
    """
    values = (user_id, user_type)

    cursor.execute(query, values)
    result = cursor.fetchone()

    if result is None:
        raise ValueError(f"User is not a {user_type}")

    return result[0]


@transactional
def register_user(db_con, user_type, payload, cursor=None) -> int:
    person_field_list = ["email", "password"]

    # password hashing (could also salt it, hash the salt, salt the hash...)
    hashed_password = hashlib.sha256(payload["password"].encode()).hexdigest()
    payload["password"] = hashed_password

    # locks tables for multiple insertions
    cursor.execute("LOCK TABLE user IN EXCLUSIVE MODE")

    query = _build_insert_query("user", person_field_list, fetch="user_id")
    values = tuple([payload[field] for field in person_field_list])

    cursor.execute(query, values)
    user = cursor.fetchone()

    if user is None:
        raise ValueError("Error creating user")

    user_id = user[0]

    logger.debug(f"User ID: {user_id}")
    return {"user_id": user_id, "user_type": user_type}

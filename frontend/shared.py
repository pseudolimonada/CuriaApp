user_ids = {
    "user_id": str,
    "manager_business_ids": list,
    "is_admin": bool
}

shared_vars = {
    "main_container": None,
    "bottom_menu": None,
    "current_order": None,
    "current_business": {}
}

endpoints_urls = {
    "LOGIN": "/login",
    "REGISTER": "/register",
    "GET_CATALOG": "/businesses/$business_id/products",
    "POST_ORDER": "/businesses/$business_id/orders",
    "GET_ORDERS": "businesses/$business_id/orders"
}

STATUS_CODES = {"SUCCESS": 200, "INVALID_CREDENTIALS": 401, "INTERNAL_ERROR": 500, "BAD_REQUEST": 400}

BG_TOP_COLOR = "#e6be7a"
BG_BOTTOM_COLOR = "#f4ac75"
MAIN_TEXT_COLOR = "#606060"



TESTING = True
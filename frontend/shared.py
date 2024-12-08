user_ids = {
    "user_id": str,
    "manager_business_ids": list
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
    "ORDERS": "/orders",
    "PRODUCTS": "/products"
}

STATUS_CODES = {"SUCCESS": 200, "INVALID_CREDENTIALS": 401, "INTERNAL_ERROR": 500, "BAD_REQUEST": 400}

PRIM_COLOR = '#f0cf7d'
SEC_COLOR = '#4c4c4c'
THIRD_COLOR = '#89f4dc'
UNF_COLOR = '#818181'

MAIN_BG_COLOR = ''
MAIN_TEXT_COLOR = ''
MAIN_DISABLED_COLOR = ''
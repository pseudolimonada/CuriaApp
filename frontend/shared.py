user_data = {
    "token": str,
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
    "GET_ORDERS": "businesses/$business_id/orders",
    "PUT_STATE" : "businesses/$business_id/orders/$order_id",
    "EDIT_CURRENT_DAY": "/businesses/$business_id/catalogs"
}

STATUS_CODES = {"SUCCESS": 200, "INVALID_CREDENTIALS": 401, "INTERNAL_ERROR": 500, "BAD_REQUEST": 400}

BG_TOP_COLOR = "#e6be7a"
BG_BOTTOM_COLOR = "#f4ac75"
PRIM_GRADIENT_COLOR_1 = "#ffd791"
PRIM_GRADIENT_COLOR_2 = "#ffc396"
SEC_GRADIENT_COLOR_1 = "#ffc270"
SEC_GRADIENT_COLOR_2 = "#ed9f60"
THIRD_GRADIENT_COLOR_1 = "#ffda9a" #"#ffeee2"
THIRD_GRADIENT_COLOR_2 = "#ffc290" #"#fae6c1"
BUTTON_OVERLAY_COLOR = "#fff791"  # CHANGE
SELECTED_GRADIENT_COLOR_1 = SEC_GRADIENT_COLOR_1
SELECTED_GRADIENT_COLOR_2 = SEC_GRADIENT_COLOR_2
DIALOG_BG_COLOR = BG_TOP_COLOR

MAIN_TEXT_COLOR = "#606060"

FILTER_BUTTON_TEXT: dict = {"Portuguese":{"waiting_validation":"Por validar", "waiting_delivery":"Por entregar", "delivered":"Entregue","rejected":"Rejeitado"}, "English":{"waiting_validation":"Waiting validation", "waiting_delivery":"Waiting delivery", "delivered":"Delivered","rejected":"Rejected"}} 

TESTING = True

configs = {
    "LANGUAGE": "English"
}
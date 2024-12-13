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

BASE_IP="http://farinhasembugs.dei.uc.pt:8080/"

endpoints_urls = {
    "LOGIN": f"{BASE_IP}users/login",
    "REGISTER": f"{BASE_IP}users/register",
    "PERMISSIONS": f"{BASE_IP}users/permissions/$business_id",
    "GET_CATALOG": f"{BASE_IP}businesses/$business_id/products",
    "POST_ORDER": f"{BASE_IP}businesses/$business_id/orders",
    "GET_ORDERS": f"{BASE_IP}businesses/$business_id/orders",
    "PUT_STATE" : f"{BASE_IP}businesses/$business_id/orders/$order_id",
    "EDIT_CURRENT_DAY": f"{BASE_IP}businesses/$business_id/catalogs"
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

FILTER_BUTTON_TEXT: dict = {
    "Portuguese": {
        "waiting_validation": "Por Validar",
        "waiting_delivery": "Por Entregar",
        "delivered": "Entregue",
        "rejected": "Rejeitado"
    },
    "English": {
        "waiting_validation": "Wait Approve",
        "waiting_delivery": "Wait Delivery",
        "delivered": "Delivered",
        "rejected": "Rejected"
    }
} 

TESTING = False

configs = {
    "LANGUAGE": "English"
}

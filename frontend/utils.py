from flet import Page, SnackBar, Text, TextThemeStyle
from shared import STATUS_CODES, user_ids, shared_vars, endpoints_urls
from string import Template
import requests

# Presents a snack bark in the page object.
def present_snack_bar(
    page: Page,
    str_to_log: str = "",
    bgcolor: str = 'Red'
):
    '''
    Presents a snack bar in page object with the given string as text.
    '''
    
    # Snack Bar creation
    snack_bar = SnackBar(
                    Text(str_to_log, theme_style=TextThemeStyle.BODY_LARGE),
                    bgcolor=bgcolor,
                    open=True
                )
    
    page.overlay.append(snack_bar)
    page.update()


# Refreshes the catalog making a request to the DB and returns the catalog.
# May return None in case of error in request.
# Catalog Structure:
#   {
#       "product_id1": {
#           "image_url":"(opt)",
#           "product_title":"...",
#           "product_description":"...",
#           "product_price":"..."
#       },
#       "product_id2": {
#           ...
#       },
#   }
#
def get_refreshed_catalog(page: Page):
    INTERNAL_ERROR_TEXT: str = "An internal error occurred, please wait and try again..."
    UNRECOGNIZED_ERROR_TEXT: str = "An unexpected error occurred, please verify if your app is updated..."
    NETWORK_ERROR_TEXT: str = "Please verify your internet connection and try again..."
    
    catalog = None
    
    headers = {
        "user_id": user_ids["user_id"],
        "manager_business_ids": user_ids["manager_business_ids"]
    }
    url_template = Template(endpoints_urls["GET_CATALOG"])
    get_catalog_url = url_template.safe_substitute(business_id=shared_vars["current_business"]["id"])
    
    try:
        # Sending request and getting response
        response = requests.get(get_catalog_url, headers=headers)
        
        # Check the response
        if response.status_code == STATUS_CODES["SUCCESS"]:
            # Save the refreshed catalog
            catalog = response["catalog"]

        elif response.status_code >= STATUS_CODES["INTERNAL_ERROR"]:
            present_snack_bar(page, INTERNAL_ERROR_TEXT, "Red")
        else:
            present_snack_bar(page, UNRECOGNIZED_ERROR_TEXT, "Red")
    except requests.exceptions.RequestException as e:
        # Handle network-related errors
        present_snack_bar(page, NETWORK_ERROR_TEXT, "Red")
    
    return catalog
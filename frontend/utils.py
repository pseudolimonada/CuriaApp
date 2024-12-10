from flet import Page, Container, ElevatedButton, ButtonStyle, LinearGradient, alignment, SnackBar, Text, TextThemeStyle, TextField, TextStyle
from shared import STATUS_CODES, user_ids, shared_vars, endpoints_urls
from string import Template
from typing import Optional, Callable, Any
import requests

# Generic textfield that can storage last value and have just numeric mode.
class Smart_TextField(TextField):
    '''
    Generic textfield that can storage last value and have just numeric mode.
    '''
    
    __page: Page
    __last_value: str = ""
    __is_numeric: bool = False
    
    def __init__(
        self,
        page: Page,
        label: str = "Label",
        hint_text: str = "Hint Text",
        disabled: Optional[bool] = False,
        numeric: Optional[bool] = False,
        expand: Optional[bool] = False,
        max_length: Optional[int] = None,
        on_blur: Optional[Callable] = None,
        label_style: Optional[TextStyle] = None,
        hint_style: Optional[TextStyle] = None,
        data: Any = None
    ):
        self.__page = page
        super().__init__(
            adaptive = True,
            label=label,
            hint_text=hint_text,
            on_change=self.change_value,
            data=data,
            disabled=disabled,
            max_length=max_length,
            expand=expand,
            label_style=label_style,
            hint_style=hint_style
        )
        self.__is_numeric = numeric
        if on_blur:
            self.on_blur = on_blur
    
    def change_value(self, e):
        '''
        Changes the current value and stores the last value.
        '''
        
        if self.__is_numeric and not e.control.value.isdigit():
            e.control.value = ''.join(filter(str.isdigit, e.control.value))
            self.__page.update()
            
        else:
            self.__last_value = self.value
            self.value = e.control.value

class Main_TextField_Container(Container):
    def __init__(
        self,
        label: Optional[str] = "Label",
        hint_text: Optional[str] = "Hint Text",
        password: Optional[bool] = False,
        can_reveal_password: Optional[bool] = False
    ):
        super().__init__(
            content=TextField(
                adaptive=True,
                label=label,
                hint_text=hint_text,
                password=password,
                can_reveal_password=can_reveal_password,
                border_radius=12,
                border_color="transparent",
                cursor_color="#606060",
                color="#606060",
                label_style=TextStyle(color="#606060"),
                hint_style=TextStyle(color="#606060")
            ),
            gradient = Primary_Gradient(),
            border_radius=10,
            alignment=alignment.center
        )

class Main_ElevatedButton_Container(Container):
    def __init__(
        self,
        text: Optional[str] = "Text",
        scale: Optional[float] = 1.0
    ):
        super().__init__(
            content=ElevatedButton(
                adaptive=True,
                text=text,
                bgcolor="transparent",
                color="#606060",
                style=ButtonStyle(
                    elevation=0,
                    overlay_color="#fff791"
                )
            ),
            gradient = Primary_Gradient(),
            border_radius=20,
            scale=scale,
            alignment=alignment.center
        )


class Primary_Gradient(LinearGradient):
    def __init__(self):
        super().__init__(
            begin=alignment.top_center,
            end=alignment.bottom_center,
            colors=[
                "#ffd791",
                "#ffc396"
            ],
        )





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
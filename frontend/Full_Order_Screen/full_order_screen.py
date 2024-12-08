from flet import Column, padding, CrossAxisAlignment, MainAxisAlignment, Page, ElevatedButton, ScrollMode, Text, icons, Divider, Row, Container, TextButton, AlertDialog, alignment, Icon, ButtonStyle
from shared import STATUS_CODES, user_ids, shared_vars, endpoints_urls
from present_snack_bar import present_snack_bar
from string import Template
import requests

class Full_Order_Screen(Column):
    '''
    Column that represents a screen for the order checks.
    Can be for confirmation of the order realization or just to check a previous order details.
    '''

    #############################################
    #              Initializations              #
    #############################################

    ###############################
    # Initializing the texts strings
    TITLE_TEXT: str = "Order Day: "
    SUBTITLE_TEXT: str = "State: "
    SUB_TITLE: str = "Order State: "
    CONFIRM_BUTTON_TEXT: str = "Confirm!"
    CANCEL_BUTTON_TEXT: str = "Cancel"
    BACK_BUTTON_TEXT: str = "Back"
    ALERT_DIALOG_TITLE_TEXT: str = "Your Order Is Done"
    ALERT_DIALOG_CONTENT_TEXT: str = "You can check order details in orders details menu."
    ALERT_DIALOG_OK_TEXT: str = "OK"
    INTERNAL_ERROR_TEXT: str = "An internal error occurred, please wait and try again..."
    UNRECOGNIZED_ERROR_TEXT: str = "An unexpected error occurred, please verify if your app is updated..."
    NETWORK_ERROR_TEXT: str = "Please verify your internet connection and try again..."

    ###############################
    # Initializing the page object
    __page: Page
    
    ###############################
    # Initializing and setting up the title and product columns
    __title_column: Column = Column(
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER
    )
    __products_column: Column = Column(
        alignment=MainAxisAlignment.START,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        scroll=ScrollMode.ADAPTIVE,
        expand=True
    )
    
    ###############################
    # Initializing the buttons row and the actual buttons
    __buttons_row: Row = Row(
        alignment=MainAxisAlignment.CENTER,
        vertical_alignment=CrossAxisAlignment.CENTER
    )
    __confirm_order_button: ElevatedButton
    __cancel_button: ElevatedButton
    __back_button: ElevatedButton
    
    ###############################
    # Initializing and setting up the alert dialog
    __alert = AlertDialog(
        modal=True,
        title=Text(ALERT_DIALOG_TITLE_TEXT),
        content=Column(
            controls=[
                Text(
                    ALERT_DIALOG_CONTENT_TEXT,
                    size=16,
                ),
                Container(
                    content=Icon(
                        name=icons.CHECK_CIRCLE,
                        size=100
                    ),
                    alignment=alignment.center
                )
            ],
            alignment=MainAxisAlignment.CENTER,
            spacing=20,
        ),
        actions_alignment=MainAxisAlignment.CENTER
    )


    #############################################
    #                Constructor                #
    #############################################

    # Constructor
    def __init__(
        self,
        page: Page
    ):
        ###############################
        # Setting the main column with all objects
        super().__init__(
            controls=[
                self.__title_column,
                self.__products_column,
                Column(
                    controls=[
                        Divider(),
                        self.__buttons_row,
                        Divider(),
                    ],
                    alignment=MainAxisAlignment.CENTER
                ),
            ],
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            expand=True
        )
        
        ###############################
        # Saving the page object
        self.__page = page
        
        ###############################
        # Setting up the buttons
        self.__confirm_order_button = ElevatedButton(
            text=self.CONFIRM_BUTTON_TEXT,
            icon=icons.CHECK,
            adaptive=True,
            on_click=self.__confirm_order,
        )
        
        self.__cancel_button = ElevatedButton(
            text=self.CANCEL_BUTTON_TEXT,
            icon=icons.CANCEL,
            adaptive=True,
            on_click=self.__cancel_order,
        )
        
        self.__back_button = ElevatedButton(
            text=self.CANCEL_BUTTON_TEXT,
            icon=icons.KEYBOARD_RETURN,
            adaptive=True,
            on_click=self.__turn_back,
            scale=1.5
        )
    
    
    #############################################
    #               Layout Methods              #
    #############################################
    
    # Sets up the confirm order layout
    def set_confirm_order_layout(self):
        # Resetting controls from before
        self.__products_column.controls.clear()
        self.__buttons_row.controls.clear()
        
        # Setting the title column
        self.__title_column.controls=[
            Divider(),
            Text(value=f"{self.TITLE_TEXT}{shared_vars["current_order"]["date"]}"),
            Divider()
        ]
        
        # Setting the products of the order
        products_dict: dict = shared_vars["current_order"]["products"]
        for product in products_dict:
            if products_dict[product]["quantity"] > 0:
                self.__products_column.controls.append(self.__create_new_product_row(product, products_dict[product]["quantity"], products_dict[product]["cost"]))
        
        # Adding the cancel and confirm buttons
        self.__buttons_row.controls.append(self.__cancel_button)
        self.__buttons_row.controls.append(self.__confirm_order_button)
        
    # Sets up the order details layout
    def set_order_details_layout(self):
        # Resetting controls from before
        self.__products_column.controls.clear()
        self.__buttons_row.controls.clear()
        
        # Setting the title column
        self.__title_column.controls=[
            Divider(),
            Text(value=f"{self.TITLE_TEXT}{shared_vars["current_order"]["date"]}"),
            Text(value=f"{self.SUBTITLE_TEXT}{shared_vars["current_order"]["state"]}"),
            Divider()
        ]
        
        # Setting the products of the order
        products_dict: dict = shared_vars["current_order"]["products"]
        for product in products_dict:
            if products_dict[product]["quantity"] > 0:
                self.__products_column.controls.append(self.__create_new_product_row(product, products_dict[product]["quantity"], products_dict[product]["cost"]))
        
        # Adding the back button
        self.__buttons_row.controls.append(self.__back_button)
    
    
    #############################################
    #         Construction Help Methods         #
    #############################################
    
    # Creates a new product row with the ordered products and their cost
    def __create_new_product_row(
        self,
        product_name: str,
        product_quantity: int,
        product_cost: str
    ):
        '''
        Creates a new product row with the ordered products and their cost.
        '''
        
        return Row(
            controls=[
                Container(
                    content=Row(
                        controls=[
                            Container(
                                content=Text(value=f"{product_name}\nx{product_quantity}"),
                                padding=padding.only(left=10, right=20),
                                expand=True
                            ),
                            Container(
                                content=Text(f"{product_quantity*float(product_cost[:-1]):.2f}€"),
                                padding=padding.only(right=10)
                            ),
                        ],
                        alignment=MainAxisAlignment.SPACE_AROUND
                    ),
                    height=80,
                    expand=True
                )
            ],
            alignment=MainAxisAlignment.SPACE_AROUND,
        )
    
    
    #############################################
    #           Button Actions Methods          #
    #############################################
    
    # Confirms the order and makes a post request to the DB
    def __confirm_order(self, e):
        '''
        Confirms the order and makes a post request to the DB
        '''
        
        ###########################################################################
        #        ------- REMOVE THIS IF CASE FOR REAL TEST !!!!!!! -------        #
        ###########################################################################
        testing = True
        if testing:
            self.__alert.actions=[
                TextButton(
                    self.ALERT_DIALOG_OK_TEXT,
                    on_click=self.__handle_close_dialog,
                    style=ButtonStyle(
                        enable_feedback=False
                    )
                ),
            ]
            self.__page.open(self.__alert)

            shared_vars["main_container"].change_screen("order_screen")
            return
        
        # Setting up the order data for the payload with only the products that actually have selected quantity
        order_data = []
        for product_title in shared_vars["current_order"]["products"].keys():
            quantity = shared_vars["current_order"]["products"][product_title]["quantity"]
            if quantity > 0:
                order_data.append(
                    {
                        "product_id": shared_vars["current_order"]["products"][product_title]["product_id"],
                        "product_quantity": quantity
                    }
                )
        
        # Setting the headers and payload json
        headers = {
            "user_id": user_ids["user_id"],
            "manager_business_ids": user_ids["manager_business_ids"]
        }
        payload = {
            "user_id": user_ids["user_id"],
            "order_date": shared_vars["current_order"]["date"],
            "order_data": order_data
        }
        
        # Setting the url for the request
        url_template = Template(endpoints_urls["POST_ORDER"])
        post_order_url = url_template.safe_substitute(business_id=shared_vars["current_business"]["id"])
        
        try:
            # Send request
            response = requests.post(post_order_url, headers=headers, json=payload)
            
            # Check the response
            if response.status_code == STATUS_CODES["SUCCESS"]:
                self.__alert.actions=[
                    TextButton(
                        self.ALERT_DIALOG_OK_TEXT,
                        on_click=self.__handle_close_dialog,
                        style=ButtonStyle(
                            enable_feedback=False
                        )
                    ),
                ]
                self.__page.open(self.__alert)
                
            elif response.status_code >= STATUS_CODES["INTERNAL_ERROR"]:
                present_snack_bar(self.__page, self.INTERNAL_ERROR_TEXT, "Red")
            else:
                present_snack_bar(self.__page, self.UNRECOGNIZED_ERROR_TEXT, "Red")
        except requests.exceptions.RequestException as e:
            # Handle network-related errors
            present_snack_bar(self.__page, self.NETWORK_ERROR_TEXT, "Red")
        
        # Change the screen for the order screen again
        shared_vars["main_container"].change_screen("order_screen")
    
    # Cancels the order and goes back to the order screen
    def __cancel_order(self, e):
        '''
        Cancels the order and goes back to the order screen
        '''
        
        shared_vars["main_container"].change_screen("order_screen")
        
    # Goes back to the check orders screen
    def __turn_back(self, e):
        '''
        Goes back to the check orders screen
        '''
        
        shared_vars["main_container"].change_screen("check_orders_screen")
    
    # Handles the close of the dialog alert
    def __handle_close_dialog(self, e):
        '''
        Handles the close of the dialog alert.
        '''
        
        self.__page.close(self.__alert)
from flet import Container, Column, MainAxisAlignment, TextStyle, ButtonStyle, ElevatedButton, TextField, Row, Page, LinearGradient, alignment, colors
from shared import STATUS_CODES, user_ids, shared_vars, endpoints_urls
from utils import Main_TextField_Container, Main_ElevatedButton_Container, present_snack_bar
import requests
from Order_Screen.order_screen import Order_Screen
from Full_Order_Screen.full_order_screen import Full_Order_Screen
from Check_Orders_Screen.check_orders_screen import Check_Orders_Screen

class Login_Screen(Column):
    '''
    Column that represents a screen for Login / Register of the user
    '''
    
    #############################################
    #              Initializations              #
    #############################################
    
    ###############################
    # Initializing the texts strings
    NAME_TEXTFIELD_TEXT: str = "User Name"
    NAME_TEXTFIELD_HINT_TEXT: str = "Insert your user name here"
    PASSWORD_TEXTFIELD_TEXT: str = "Password"
    PASSWORD_TEXTFIELD_HINT_TEXT: str = "Insert your password here"
    LOGIN_BUTTON_TEXT: str = "LOGIN"
    REGISTER_BUTTON_TEXT: str = "REGISTER"
    INVALID_LOGIN_ERROR_TEXT: str = "Invalid Login Credentials..."
    INTERNAL_ERROR_TEXT: str = "An internal error occurred, please wait and try again..."
    BAD_REQUEST_ERROR_TEXT: str = "An error occurred, please verify if your app is updated..."
    UNRECOGNIZED_ERROR_TEXT: str = "An unexpected error occurred, please verify if your app is updated..."
    NETWORK_ERROR_TEXT: str = "Please verify your internet connection and try again..."
    
    ###############################
    # Initializing the page object
    __page: Page
    
    ###############################
    # Initializing and setting up the textfields
    name_textfield: Main_TextField_Container = Main_TextField_Container(
        label=NAME_TEXTFIELD_TEXT,
        hint_text=NAME_TEXTFIELD_HINT_TEXT
    )
    password_textfield: Main_TextField_Container = Main_TextField_Container(
        label=PASSWORD_TEXTFIELD_TEXT,
        hint_text=PASSWORD_TEXTFIELD_HINT_TEXT,
        password=True,
        can_reveal_password=True
    )
    credentials_column: Column
    
    # Buttons
    login_button: Main_ElevatedButton_Container = Main_ElevatedButton_Container(
        text=LOGIN_BUTTON_TEXT,
        scale=1.5
    )
    register_button: Main_ElevatedButton_Container = Main_ElevatedButton_Container(
        text=REGISTER_BUTTON_TEXT
    )
    login_register_column: Column
    
    # Constructor
    def __init__(
        self,
        page: Page
    ):
        super().__init__(
            alignment=MainAxisAlignment.SPACE_EVENLY,
            expand=True
        )
        
        self.__page = page
        
        # Setting the column with the text fields
        self.credentials_column = Column(
            controls=[
                Row(controls=[self.name_textfield], alignment=MainAxisAlignment.CENTER),
                Row(controls=[self.password_textfield], alignment=MainAxisAlignment.CENTER)
            ],
            alignment=MainAxisAlignment.CENTER
        )
        
        # Setting the column with the buttons
        self.login_button.content.on_click = self.login
        self.register_button.content.on_click = self.register
        self.login_register_column = Column(
            controls=[
                Row(controls=[self.login_button], alignment=MainAxisAlignment.CENTER),
                Row(controls=[self.register_button], alignment=MainAxisAlignment.CENTER),
            ],
            alignment=MainAxisAlignment.CENTER,
            spacing=20
        )
        
        # Setting the controls of the screen (column) with all elements
        self.controls = [
            self.credentials_column,
            self.login_register_column
        ]

    def login(self, e):
        '''
        Verifies in DB if the inserted credentials exist and are valid. If they are makes the transition to the orders screen.
        '''

        ###########################################################################
        #        ------- REMOVE THIS IF CASE FOR REAL TEST !!!!!!! -------        #
        ###########################################################################
        if self.name_textfield.content.value == "" and self.password_textfield.content.value == "":
            self.__init_client_mode()
            shared_vars["main_container"].change_screen("order_screen")
        else:

            # Defining the payload
            payload = {
                "user_name": self.name_textfield.content.value,
                "user_password": self.password_textfield.content.value
            }
            try:
                # Sending request and getting response
                response = requests.post(endpoints_urls["LOGIN"], json=payload)
                
                # Check the response
                if response.status_code == STATUS_CODES["SUCCESS"]:
                    # Set user ids
                    user_ids["user_id"] = response["user_id"]
                    user_ids["manager_business_ids"] = response["manager_business_ids"]
                    self.__init_client_mode()
                    
                    # Change screen
                    shared_vars["main_container"].change_screen("order_screen")
                elif response.status_code == STATUS_CODES["INVALID_CREDENTIALS"]:
                    present_snack_bar(self.__page, self.INVALID_LOGIN_ERROR_TEXT, "Red")
                elif response.status_code >= STATUS_CODES["INTERNAL_ERROR"]:
                    present_snack_bar(self.__page, self.INTERNAL_ERROR_TEXT, "Red")
                elif response.status_code == STATUS_CODES["BAD_REQUEST"]:
                    present_snack_bar(self.__page, self.BAD_REQUEST_ERROR_TEXT, "Red")
                else:
                    present_snack_bar(self.__page, self.UNRECOGNIZED_ERROR_TEXT, "Red")
            except requests.exceptions.RequestException as e:
                # Handle network-related errors
                present_snack_bar(self.__page, self.NETWORK_ERROR_TEXT, "Red")
            
    def register(self, e):
        '''
        Registers the user with the respective credentials in DB and makes the transition to the orders screen.
        '''
        
        ###########################################################################
        #        ------- REMOVE THIS IF CASE FOR REAL TEST !!!!!!! -------        #
        ###########################################################################
        if self.name_textfield.content.value == "" and self.password_textfield.content.value == "":
            self.__init_client_mode()
            shared_vars["main_container"].change_screen("order_screen")
        else:

            # Defining the payload
            payload = {
                "user_name": self.name_textfield.content.value,
                "user_password": self.password_textfield.content.value
            }

            try:
                # Sending request and getting response
                response = requests.post(endpoints_urls["REGISTER"], json=payload)
                
                # Check the response
                if response.status_code == STATUS_CODES["SUCCESS"]:
                    # Set user ids
                    user_ids["user_id"] = response["user_id"]
                    user_ids["manager_business_ids"] = response["manager_business_ids"]
                    self.__init_client_mode()
                    
                    # Change screen
                    shared_vars["main_container"].change_screen("order_screen")
                elif response.status_code == STATUS_CODES["INVALID_CREDENTIALS"]:
                    present_snack_bar(self.__page, self.INVALID_LOGIN_ERROR_TEXT, "Red")
                elif response.status_code >= STATUS_CODES["INTERNAL_ERROR"]:
                    present_snack_bar(self.__page, self.INTERNAL_ERROR_TEXT, "Red")
                elif response.status_code == STATUS_CODES["BAD_REQUEST"]:
                    present_snack_bar(self.__page, self.BAD_REQUEST_ERROR_TEXT, "Red")
                else:
                    present_snack_bar(self.__page, self.UNRECOGNIZED_ERROR_TEXT, "Red")
            except requests.exceptions.RequestException as e:
                # Handle network-related errors
                present_snack_bar(self.__page, self.NETWORK_ERROR_TEXT, "Red")
    
    # Initializes all screen of a client user         
    def __init_client_mode(self):
        '''
        Initializes all screen of a client user
        '''
        
        order_screen = Order_Screen(self.__page)
        full_order_screen = Full_Order_Screen(self.__page)
        check_orders_screen = Check_Orders_Screen(self.__page)
        
        shared_vars["main_container"].add_screen_to_list(order_screen, "order_screen")
        shared_vars["main_container"].add_screen_to_list(full_order_screen, "full_order_screen")
        shared_vars["main_container"].add_screen_to_list(check_orders_screen,"check_orders_screen")
    
        
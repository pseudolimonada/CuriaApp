from flet import Column, MainAxisAlignment, Row, Page, FontWeight, TextAlign, Container, alignment, padding
from shared import TESTING, STATUS_CODES, user_data, shared_vars, endpoints_urls, MAIN_TEXT_COLOR, configs
from utils import Main_TextField_Container, Main_ElevatedButton_Container, Text, present_snack_bar
import requests
from string import Template
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
    NAME_TEXTFIELD_TEXT: dict = {
        "English": "Username",
        "Portuguese": "Username"
    }
    NAME_TEXTFIELD_HINT_TEXT: dict = {
        "English": "Insert your username here",
        "Portuguese": "Insira aqui o seu username"
    }
    PASSWORD_TEXTFIELD_TEXT: dict = {
        "English": "Password",
        "Portuguese": "Password"
    }
    PASSWORD_TEXTFIELD_HINT_TEXT: dict = {
        "English": "Insert your password here",
        "Portuguese": "Insira aqui a sua password"
    }
    LOGIN_BUTTON_TEXT: dict = {
        "English": "LOGIN",
        "Portuguese": "LOGIN"
    }
    REGISTER_BUTTON_TEXT: dict = {
        "English": "REGISTER",
        "Portuguese": "REGISTAR"
    }
    INVALID_LOGIN_ERROR_TEXT: dict = {
        "English": "Invalid Login Credentials...",
        "Portuguese": "Credenciais de login inválidas..."
    }
    INTERNAL_ERROR_TEXT: dict = {
        "English": "An internal error occurred, please wait and try again...",
        "Portuguese": "Ocorreu um erro interno, por favor, espere e tente novamente..."
    }
    BAD_REQUEST_TEXT: dict = {
        "English": "An unexpected error occurred, please verify if your app is updated...",
        "Portuguese": "Ocorreu um erro inesperado, por favor, verifique se a sua aplicação está atualizada..."
    }
    UNRECOGNIZED_ERROR_TEXT: dict = {
        "English": "An unexpected error occurred, please verify if your app is updated...",
        "Portuguese": "Ocorreu um erro inesperado, por favor, verifique se a sua aplicação está atualizada..."
    }
    NETWORK_ERROR_TEXT: dict = {
        "English": "Please verify your internet connection and try again...",
        "Portuguese": "Por favor verifique a sua conexão à internet e tente novamente..."
    }
    
    ###############################
    # Initializing the page object
    __page: Page
    
    __curia_name: Container = Container(
        content=Text(
            value="CURIA",
            size=35,
            weight=FontWeight.BOLD,
            color=MAIN_TEXT_COLOR,
            text_align=TextAlign.CENTER,
            font_family="Gliker_SemiBold"
        ),
        alignment=alignment.center,
        padding=padding.only(top=1, bottom=20, right=10, left=10)
    )
    
    ###############################
    # Initializing and setting up the textfields
    name_textfield: Main_TextField_Container
    password_textfield: Main_TextField_Container
    credentials_column: Column
    
    # Buttons
    login_button: Main_ElevatedButton_Container
    register_button: Main_ElevatedButton_Container
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
        
        # Initializing the textfield
        self.name_textfield = Main_TextField_Container(
            label=self.NAME_TEXTFIELD_TEXT[configs["LANGUAGE"]],
            hint_text=self.NAME_TEXTFIELD_HINT_TEXT[configs["LANGUAGE"]]
        )
        self.password_textfield = Main_TextField_Container(
            label=self.PASSWORD_TEXTFIELD_TEXT[configs["LANGUAGE"]],
            hint_text=self.PASSWORD_TEXTFIELD_HINT_TEXT[configs["LANGUAGE"]],
            password=True,
            can_reveal_password=True
        )
        
        # Setting the column with the text fields
        self.credentials_column = Column(
            controls=[
                self.__curia_name,
                Row(controls=[self.name_textfield], alignment=MainAxisAlignment.CENTER),
                Row(controls=[self.password_textfield], alignment=MainAxisAlignment.CENTER)
            ],
            alignment=MainAxisAlignment.CENTER
        )
        
        # Initializing the buttons
        self.login_button = Main_ElevatedButton_Container(
            text=self.LOGIN_BUTTON_TEXT[configs["LANGUAGE"]],
            scale=1.5
        )
        self.register_button = Main_ElevatedButton_Container(
            text=self.REGISTER_BUTTON_TEXT[configs["LANGUAGE"]]
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
        if TESTING:
            if self.name_textfield.content.value == "admin" and self.password_textfield.content.value == "admin":
                user_data["is_admin"] = True
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
                    # Getting the user data
                    response_data = response.json()
                    user_data["token"] = response_data.get("token")
                    self.__get_permissions()

                elif response.status_code == STATUS_CODES["INVALID_CREDENTIALS"]:
                    present_snack_bar(self.__page, self.INVALID_LOGIN_ERROR_TEXT[configs["LANGUAGE"]], "Red")
                elif response.status_code >= STATUS_CODES["INTERNAL_ERROR"]:
                    present_snack_bar(self.__page, self.INTERNAL_ERROR_TEXT[configs["LANGUAGE"]], "Red")
                elif response.status_code == STATUS_CODES["BAD_REQUEST"]:
                    present_snack_bar(self.__page, self.BAD_REQUEST_ERROR_TEXT[configs["LANGUAGE"]], "Red")
                else:
                    present_snack_bar(self.__page, self.UNRECOGNIZED_ERROR_TEXT[configs["LANGUAGE"]], "Red")
            except requests.exceptions.RequestException as e:
                # Handle network-related errors
                present_snack_bar(self.__page, self.NETWORK_ERROR_TEXT[configs["LANGUAGE"]], "Red")
            
    def register(self, e):
        '''
        Registers the user with the respective credentials in DB and makes the transition to the orders screen.
        '''
        
        ###########################################################################
        #        ------- REMOVE THIS IF CASE FOR REAL TEST !!!!!!! -------        #
        ###########################################################################
        if TESTING:
            if self.name_textfield.content.value == "admin" and self.password_textfield.content.value == "admin":
                user_data["is_admin"] = True
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
                    # Getting the user data
                    response_data = response.json()
                    user_data["token"] = response_data.get("token")
                    self.__get_permissions()
                    
                elif response.status_code == STATUS_CODES["INVALID_CREDENTIALS"]:
                    present_snack_bar(self.__page, self.INVALID_LOGIN_ERROR_TEXT[configs["LANGUAGE"]], "Red")
                elif response.status_code >= STATUS_CODES["INTERNAL_ERROR"]:
                    present_snack_bar(self.__page, self.INTERNAL_ERROR_TEXT[configs["LANGUAGE"]], "Red")
                elif response.status_code == STATUS_CODES["BAD_REQUEST"]:
                    present_snack_bar(self.__page, self.BAD_REQUEST_ERROR_TEXT[configs["LANGUAGE"]], "Red")
                else:
                    present_snack_bar(self.__page, self.UNRECOGNIZED_ERROR_TEXT[configs["LANGUAGE"]], "Red")
            except requests.exceptions.RequestException as e:
                # Handle network-related errors
                present_snack_bar(self.__page, self.NETWORK_ERROR_TEXT[configs["LANGUAGE"]], "Red")
    
    # Gets the permissions of the user to know if it is an admin or not
    def __get_permissions(self):
        '''
        Gets the permissions of the user to know if it is an admin or not
        '''

        headers = {
            "Authorization": f"{user_data["token"]}"
        }
        
        url_template = Template(endpoints_urls["PERMISSIONS"])
        get_permissions_url = url_template.safe_substitute(business_id=shared_vars["current_business"]["id"])
        
        try:
            # Sending request and getting response
            response = requests.get(get_permissions_url, headers=headers)
            
            # Check the response
            if response.status_code == STATUS_CODES["SUCCESS"]:
                # Getting the user data
                response_data = response.json()
                user_data["is_admin"] = response_data.get("is_admin")
                self.__init_client_mode()
                # Change screen
                shared_vars["main_container"].change_screen("order_screen")
                
            elif response.status_code == STATUS_CODES["INVALID_CREDENTIALS"]:
                present_snack_bar(self.__page, self.INVALID_LOGIN_ERROR_TEXT[configs["LANGUAGE"]], "Red")
            elif response.status_code >= STATUS_CODES["INTERNAL_ERROR"]:
                present_snack_bar(self.__page, self.INTERNAL_ERROR_TEXT[configs["LANGUAGE"]], "Red")
            elif response.status_code == STATUS_CODES["BAD_REQUEST"]:
                present_snack_bar(self.__page, self.BAD_REQUEST_ERROR_TEXT[configs["LANGUAGE"]], "Red")
            else:
                present_snack_bar(self.__page, self.UNRECOGNIZED_ERROR_TEXT[configs["LANGUAGE"]], "Red")
        except requests.exceptions.RequestException as e:
            # Handle network-related errors
            present_snack_bar(self.__page, self.NETWORK_ERROR_TEXT[configs["LANGUAGE"]], "Red")
    
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
    
        
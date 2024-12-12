from flet import TextAlign, FontWeight, Column, padding, CrossAxisAlignment, MainAxisAlignment, Page, ElevatedButton, ScrollMode, Text, icons, Row, Container, TextButton, AlertDialog, alignment, Icon, ButtonStyle
from shared import TESTING, MAIN_TEXT_COLOR, DIALOG_BG_COLOR, BUTTON_OVERLAY_COLOR, STATUS_CODES, user_data, shared_vars, endpoints_urls, configs, FILTER_BUTTON_TEXT
from utils import Primary_Gradient, Secondary_Gradient, Third_Gradient, present_snack_bar

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
    TITLE_TEXT: dict = {
        "English": "Order Day: ",
        "Portuguese": "Pedido para o dia: "
    }
    SUBTITLE_TEXT: dict = {
        "English": "State: ",
        "Portuguese": "Estado: "
    }
    TOTAL_COST_TEXT: dict = {
        "English": "Total Cost: ",
        "Portuguese": "Preço Total: "
    }
    CONFIRM_BUTTON_TEXT: dict = {
        "English": "Confirm!",
        "Portuguese": "Confirmar!"
    }
    CANCEL_BUTTON_TEXT: dict = {
        "English": "Cancel",
        "Portuguese": "Cancelar"
    }
    BACK_BUTTON_TEXT: dict = {
        "English": "Back",
        "Portuguese": "Voltar"
    }
    APPROVE_BUTTON_TEXT: dict = {
        "English": "Approve",
        "Portuguese": "Aprovar"
    }
    DENY_BUTTON_TEXT: dict = {
        "English": "Deny",
        "Portuguese": "Negar"
    }
    ALERT_DIALOG_TITLE_TEXT: dict = {
        "English": "Your Order Is Done",
        "Portuguese": "Encomenda Realizada"
    }
    ALERT_DIALOG_CONTENT_TEXT: dict = {
        "English": "You can check order details in orders details menu.",
        "Portuguese": "Pode confirmar os detalhes do seu pedido na página de detalhes das encomendas."
    }
    ALERT_DIALOG_OK_TEXT: dict = {
        "English": "OK",
        "Portuguese": "OK"
    }
    REJECTED_ORDER_TEXT: dict = {
        "English": "Order rejected with success",
        "Portuguese": "Encomenda rejeitada com sucesso"
    }
    ACCEPTED_ORDER_TEXT: dict = {
        "English": "Order accepted with success",
        "Portuguese": "Encomenda aceite com sucesso"
    }
    INTERNAL_ERROR_TEXT: dict = {
        "English": "An internal error occurred, please wait and try again...",
        "Portuguese": "Ocorreu um erro interno, por favor, espere e tente novamente..."
    }
    UNRECOGNIZED_ERROR_TEXT: dict = {
        "English": "An unexpected error occurred, please verify if your app is updated...",
        "Portuguese": "Ocorreu um erro inesperado, por favor, verifique se a sua aplicação está atualizada..."
    }
    NETWORK_ERROR_TEXT: dict = {
        "English": "Please verify your internet connection and try again...",
        "Portuguese": "Por favor verifique a sua conexão à internet e tente novamente..."
    }
    BAD_REQUEST_TEXT: dict = {
        "English": "An unexpected error occurred, please verify if your app is updated...",
        "Portuguese": "Ocorreu um erro inesperado, por favor, verifique se a sua aplicação está atualizada..."
    }


    ###############################
    # Initializing the page object
    __page: Page
    
    ###############################
    # Initializing total cost track variable
    __current_total_cost: float = 0
    
    ###############################
    # Initializing and setting up the title and product columns
    __title_column: Container = Container(
        content=Column(
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            spacing=5
        ),
        alignment=alignment.center,
        gradient=Secondary_Gradient(),
        padding=padding.only(top=10, bottom=15),
        border_radius=12,
    )
    __products_column: Column = Column(
        alignment=MainAxisAlignment.START,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        scroll=ScrollMode.ADAPTIVE,
        expand=True
    )
    
    ###############################
    # Initializing the buttons row and the actual buttons
    __buttons_row: Container = Container(
        content=Row(
            alignment=MainAxisAlignment.CENTER,
            vertical_alignment=CrossAxisAlignment.CENTER
        ),
        border_radius=12,
        gradient=Secondary_Gradient(),
        padding=padding.only(top=20, bottom=25),
        alignment=alignment.center
    )
    __confirm_order_button: Container = Container(
        alignment=alignment.center,
        gradient=Primary_Gradient(),
        border_radius=20,
    )
    __cancel_button: Container = Container(
        alignment=alignment.center,
        gradient=Primary_Gradient(),
        border_radius=20,
    )
    __back_button: Container = Container(
        alignment=alignment.center,
        gradient=Primary_Gradient(),
        border_radius=20,
    )
    __approve_order_button: Container = Container(
        alignment=alignment.center,
        gradient=Primary_Gradient(),
        border_radius=20,
    )
    __deny_order_button: Container = Container(
        alignment=alignment.center,
        gradient=Primary_Gradient(),
        border_radius=20,
    )
    
    ###############################
    # Initializing and setting up the alert dialog
    __alert = AlertDialog(
        modal=True,
        adaptive=True,
        bgcolor=DIALOG_BG_COLOR,
        icon=Icon(
            name=icons.CHECK_CIRCLE,
            color="#34c862",
            size=100
        ),
        title=Text(
            color=MAIN_TEXT_COLOR
        ),
        content=Text(
            color=MAIN_TEXT_COLOR,
            size=16,
        ),
        actions_alignment=MainAxisAlignment.END
    )
    
    __general_message: AlertDialog
    __rejected_message: AlertDialog = AlertDialog(
        modal=True,
        title=Text(
            color=MAIN_TEXT_COLOR
        ),
        content=Column(
            controls=[
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
    __accepted_message: AlertDialog = AlertDialog(
        modal=True,
        title=Text(
            color=MAIN_TEXT_COLOR
        ),
        content=Column(
            controls=[
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
                Column(
                    controls=[
                        self.__title_column,
                        self.__products_column,
                    ],
                    alignment=MainAxisAlignment.START,
                    expand=True
                ),
                self.__buttons_row
            ],
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            expand=True
        )
        
        ###############################
        # Saving the page object
        self.__page = page
        
        ###############################
        # Setting up the buttons
        self.__back_button.content = ElevatedButton(
            text=self.BACK_BUTTON_TEXT[configs["LANGUAGE"]],
            icon=icons.KEYBOARD_RETURN,
            icon_color="#606060",
            adaptive=True,

            on_click=self.__turn_back,
            bgcolor="transparent",
            color="#606060",
            style=ButtonStyle(
                padding=padding.symmetric(10, 70),
                elevation=0,
                overlay_color=BUTTON_OVERLAY_COLOR
            )
        )
        
        if user_data["is_admin"]:
            self.__back_button.scale=0.8
            self.__approve_order_button.content = ElevatedButton(
                text=self.APPROVE_BUTTON_TEXT[configs["LANGUAGE"]],
                icon=icons.CHECK,
                icon_color="#606060",
                adaptive=True,
                on_click=self.__change_order_state,
                data="approve",
                bgcolor="transparent",
                color="#606060",
                style=ButtonStyle(
                    elevation=0,
                    overlay_color=BUTTON_OVERLAY_COLOR
                )
            )
            self.__deny_order_button.content = ElevatedButton(
                text=self.DENY_BUTTON_TEXT[configs["LANGUAGE"]],
                icon=icons.CANCEL,
                icon_color="#606060",
                adaptive=True,
                on_click=self.__change_order_state,
                data="reject",
                bgcolor="transparent",
                color="#606060",
                style=ButtonStyle(
                    elevation=0,
                    overlay_color=BUTTON_OVERLAY_COLOR
                )
            )
        else:
            self.__back_button.scale=1.2
            self.__confirm_order_button.content = ElevatedButton(
                text=self.CONFIRM_BUTTON_TEXT[configs["LANGUAGE"]],
                icon=icons.CHECK,
                icon_color="#606060",
                adaptive=True,
                on_click=self.__confirm_order,
                bgcolor="transparent",
                color="#606060",
                style=ButtonStyle(
                    elevation=0,
                    overlay_color=BUTTON_OVERLAY_COLOR
                )
            )
            self.__cancel_button.content = ElevatedButton(
                text=self.CANCEL_BUTTON_TEXT[configs["LANGUAGE"]],
                icon=icons.CANCEL,
                icon_color="#606060",
                adaptive=True,
                on_click=self.__cancel_order,
                bgcolor="transparent",
                color="#606060",
                style=ButtonStyle(
                    elevation=0,
                    overlay_color=BUTTON_OVERLAY_COLOR
                )
            )
        
        self.__alert.actions=[
            Container(
                content = ElevatedButton(
                    text=self.ALERT_DIALOG_OK_TEXT[configs["LANGUAGE"]],
                    adaptive=True,
                    on_click=self.__handle_close_dialog,
                    bgcolor="transparent",
                    color="#606060",
                    style=ButtonStyle(
                        elevation=0,
                        overlay_color=BUTTON_OVERLAY_COLOR
                    )
                ),
                gradient=Primary_Gradient(),
                border_radius=20
            )
        ]
        self.__alert.title.value=self.ALERT_DIALOG_TITLE_TEXT[configs["LANGUAGE"]]
        self.__alert.content.value=self.ALERT_DIALOG_CONTENT_TEXT[configs["LANGUAGE"]]
        
        self.__rejected_message.actions=[
            TextButton(
                text = "Ok",
                data = "deny",
                on_click=self.__handle_close,
                style=ButtonStyle(
                    enable_feedback=False
                )
            ),
        ]
        self.__rejected_message.title.value=self.REJECTED_ORDER_TEXT[configs["LANGUAGE"]]
    
        self.__accepted_message.actions=[
            TextButton(
                "Ok",
                data = "approve",
                on_click=self.__handle_close,
                style=ButtonStyle(
                    enable_feedback=False
                )
            ),
        ]
        self.__accepted_message.title.value=self.ACCEPTED_ORDER_TEXT[configs["LANGUAGE"]]
    
    #############################################
    #               Layout Methods              #
    #############################################
    
    # Sets up the confirm order layout
    def set_confirm_order_layout(self):
        # Resetting controls from before
        self.__products_column.controls.clear()
        self.__buttons_row.content.controls.clear()
        self.__current_total_cost = 0
        
        # Setting the products of the order
        products_dict: dict = shared_vars["current_order"]["products"]
        for product in products_dict:
            if products_dict[product]["quantity"] > 0:
                self.__products_column.controls.append(self.__create_new_product_row(product, products_dict[product]["quantity"], products_dict[product]["cost"]))
        
        # Setting the title column
        self.__title_column.content.controls=[
            Text(
                value=f"{shared_vars["current_business"]["name"]}",
                size=25,
                text_align=TextAlign.CENTER,
                width=FontWeight.BOLD,
                color=MAIN_TEXT_COLOR
            ),
            Text(
                value=f"{self.TITLE_TEXT[configs["LANGUAGE"]]}{shared_vars["current_order"]["date"]}",
                text_align=TextAlign.CENTER,
                color=MAIN_TEXT_COLOR
            ),
            Text(
                value=f"{self.TOTAL_COST_TEXT[configs["LANGUAGE"]]}{self.__current_total_cost:.2f}€",
                text_align=TextAlign.CENTER,
                width=FontWeight.BOLD,
                color=MAIN_TEXT_COLOR
            )
        ]
        
        # Adding the cancel and confirm buttons
        self.__buttons_row.content.controls.append(self.__cancel_button)
        self.__buttons_row.content.controls.append(self.__confirm_order_button)
        
    # Sets up the order details layout
    def set_order_details_layout(self):
        # Resetting controls from before
        self.__products_column.controls.clear()
        self.__buttons_row.content.controls.clear()
        self.__current_total_cost = 0
        
        # Setting the products of the order
        products_dict: dict = shared_vars["current_order"]["products"]
        for product in products_dict:
            if products_dict[product]["quantity"] > 0:
                self.__products_column.controls.append(self.__create_new_product_row(product, products_dict[product]["quantity"], products_dict[product]["cost"]))
        
        # Setting the title column
        self.__title_column.content.controls=[
            Text(
                value=f"{shared_vars["current_business"]["name"]}",
                size=25,
                text_align=TextAlign.CENTER,
                width=FontWeight.BOLD,
                color=MAIN_TEXT_COLOR
            ),
            Text(
                value=f"{self.TITLE_TEXT[configs["LANGUAGE"]]}{shared_vars["current_order"]["date"]}",
                text_align=TextAlign.CENTER,
                color=MAIN_TEXT_COLOR
            ),
            Text(
                value=f"{self.SUBTITLE_TEXT[configs["LANGUAGE"]]}{FILTER_BUTTON_TEXT[configs["LANGUAGE"]][shared_vars["current_order"]["state"]]}",
                text_align=TextAlign.CENTER,
                color=MAIN_TEXT_COLOR
            ),
            Text(
                value=f"{self.TOTAL_COST_TEXT[configs["LANGUAGE"]]}{self.__current_total_cost:.2f}€",
                text_align=TextAlign.CENTER,
                width=FontWeight.BOLD,
                color=MAIN_TEXT_COLOR
            )
        ]
        
        
        # TODO: need to change the logic because if it is an adm and already accepted or denied, should not appear this buttons
        if user_data["is_admin"] and shared_vars["current_order"]["state"] == "waiting_validation":
            self.__back_button.scale = 0.8
            self.__buttons_row.content.controls.append(
                Container(
                    content=Column(
                        controls=[
                            Row(
                                controls=[
                                    self.__deny_order_button,
                                    self.__approve_order_button
                                ],
                                alignment=MainAxisAlignment.CENTER
                            ),
                            self.__back_button
                        ],
                        alignment=MainAxisAlignment.CENTER,
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        spacing=5
                    ),
                    alignment=alignment.center
                )
            )
        else:
            # Adding the back button
            self.__back_button.scale = 1.2
            self.__buttons_row.content.controls.append(self.__back_button)

    
    
    #############################################
    #         Construction Help Methods         #
    #############################################
    
    # Creates a new product row with the ordered products and their cost
    def __create_new_product_row(
        self,
        product_name: str,
        product_quantity: int,
        product_cost: float
    ):
        '''
        Creates a new product row with the ordered products and their cost.
        '''

        total_cost = product_quantity*product_cost
        self.__current_total_cost += total_cost
        
        return Container(
            content=Row(
                controls=[
                    Container(
                        content=Row(
                            controls=[
                                Container(
                                    content=Text(
                                        value=f"{product_name}\nx{product_quantity}",
                                        color = MAIN_TEXT_COLOR
                                    ),
                                    padding=padding.only(left=5, right=15),
                                    expand=True
                                ),
                                Container(
                                    content=Text(
                                        value=f"{total_cost:.2f}€",
                                        color = MAIN_TEXT_COLOR
                                    ),
                                    padding=padding.only(right=5)
                                ),
                            ],
                            alignment=MainAxisAlignment.SPACE_AROUND
                        ),
                        height=60,
                        expand=True,
                        gradient = Third_Gradient(),
                        border_radius=15,
                        alignment=alignment.center
                    )
                ],
                alignment=MainAxisAlignment.CENTER
            ),
            padding=padding.symmetric(2.5, 10),
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
        if TESTING:
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
            "Authorization": f"{user_data["token"]}"
        }
        payload = {
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
                self.__page.open(self.__alert)
                
            elif response.status_code >= STATUS_CODES["INTERNAL_ERROR"]:
                present_snack_bar(self.__page, self.INTERNAL_ERROR_TEXT[configs["LANGUAGE"]], "Red")
            else:
                present_snack_bar(self.__page, self.UNRECOGNIZED_ERROR_TEXT[configs["LANGUAGE"]], "Red")
        except requests.exceptions.RequestException as e:
            # Handle network-related errors
            present_snack_bar(self.__page, self.NETWORK_ERROR_TEXT[configs["LANGUAGE"]], "Red")
        
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
    

    def __change_order_state(self, e):
        '''
        Changes the order state according to the pressed button
        '''
        
        match e.control.data:
            case "approve":
                new_state = "waiting_delivery"
                self.__general_message = self.__accepted_message
            case "reject":
                new_state = "rejected"
                self.__general_message = self.__rejected_message

        #Beginning of test

        if TESTING:
            self.__page.open(self.__general_message)
            shared_vars["main_container"].change_screen("check_orders_screen")
            return

        headers = {
            "Authorization": f"{user_data["token"]}"
        }
        payload = {
            "order_state" : new_state
        }
        url_template = Template(endpoints_urls["PUT_STATE"])
        put_state_url = url_template.safe_substitute(business_id=shared_vars["current_business"]["id"], order_id = shared_vars["current_order"]["order_id"])
        
        try:
            response = requests.put(put_state_url,headers=headers,json=payload)

            if response.status_code == STATUS_CODES["SUCCESS"]:
                self.__page.open(self.__general_message)
            elif response.status_code == STATUS_CODES["BAD_REQUEST"]:
                present_snack_bar(self.__page, self.BAD_REQUEST_TEXT[configs["LANGUAGE"]],"Red")
            elif response.status_code == STATUS_CODES["INTERNAL_ERROR"]:
                present_snack_bar(self.__page, self.INTERNAL_ERROR_TEXT[configs["LANGUAGE"]], "Red")
            else:
                present_snack_bar(self.__page, self.UNRECOGNIZED_ERROR_TEXT[configs["LANGUAGE"]], "Red")
        except requests.exceptions.RequestException as e:
            # Handle network-related errors
            present_snack_bar(self.__page, self.NETWORK_ERROR_TEXT[configs["LANGUAGE"]], "Red")

        shared_vars["main_container"].change_screen("check_orders_screen")
    
    # Handles the close of the dialog alert
    def __handle_close_dialog(self, e):
        '''
        Handles the close of the dialog alert.
        '''
        
        self.__page.close(self.__alert)

    #Handles the close of __rejected_messsage / __accepted_message
    def __handle_close(self, e):
        if e.control.data == "deny":
            self.__page.close(self.__rejected_message)
        else:
            self.__page.close(self.__accepted_message)

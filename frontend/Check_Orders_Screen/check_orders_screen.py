from flet import Column, TextAlign, MainAxisAlignment, ElevatedButton, Row, Page, ScrollMode, ButtonStyle, padding, Container, Text, CircleBorder, BorderSide, VisualDensity, TextStyle, Padding, alignment
from utils import get_refreshed_catalog, present_snack_bar, Selected_Gradient, Secondary_ElevatedButton_Container, Smart_TextField, Primary_Gradient, Secondary_Gradient, Third_Gradient
from shared import shared_vars, user_data, endpoints_urls, STATUS_CODES,FILTER_BUTTON_TEXT, TESTING, MAIN_TEXT_COLOR, BUTTON_OVERLAY_COLOR, configs
import requests
from string import Template

class Check_Orders_Screen(Column):
    '''
    Column that displays all the orders a user has made
    '''

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

    #Initializing useful variables
    __page = Page

    __days_row: Row = Row(alignment = MainAxisAlignment.START, scroll = ScrollMode.ADAPTIVE)

    __filters_row: Row = Row(alignment = MainAxisAlignment.CENTER, wrap=True)

    __orders_column: Column = Column(alignment = MainAxisAlignment.START, scroll = ScrollMode.ADAPTIVE, expand = True)

    __current_date: str

    __current_filter = "All"

    __orders : list = []

    __catalog: dict

    __buttons_dict : dict ={}
    
    __waiting_validation_button: Container
    __delivered_button: Container
    __waiting_delivery_button: Container
    __rejected_button: Container
    __buttons_dict: dict
    
    
    #Constructor
    def __init__(self, page: Page):
        super().__init__(alignment = MainAxisAlignment.SPACE_BETWEEN, expand = True)

        self.__page = page
        
        self.refresh_data()

        self.__waiting_validation_button = self.__create_filter_button("waiting_validation")
        self.__delivered_button = self.__create_filter_button("delivered")
        self.__waiting_delivery_button = self.__create_filter_button("waiting_delivery")
        self.__rejected_button = self.__create_filter_button("rejected")
        self.__buttons_dict = {
            "waiting_validation": self.__waiting_validation_button,
            "delivered": self.__delivered_button,
            "waiting_delivery": self.__waiting_delivery_button,
            "rejected": self.__rejected_button
        }

        self.__create_filters_row()
        self.__fill_orders_column()

        # Creating a column that joins order, filters and pages menu rows
        order_row_and_pages_menu_row = Container(
            content= Column(
                controls=[
                    shared_vars["bottom_menu"]
                ],
                alignment=MainAxisAlignment.CENTER,
                spacing=20,
            ),       
            padding = Padding(left=10,right=10,top=10,bottom=5),
            border_radius=12,
            gradient=Secondary_Gradient(),
            alignment=alignment.center,
        )

        # Updating controls of the screen
        self.controls = [
            Column(
                controls=[
                    Container(
                        content=self.__filters_row,
                        padding = Padding(left=10,right=10,top=10,bottom=10),
                        border_radius=12,
                        gradient=Secondary_Gradient(),
                        alignment=alignment.center
                    ),
                    self.__orders_column,
                ],
                alignment=MainAxisAlignment.START,
                expand=True
            ),
            order_row_and_pages_menu_row,        
        ]
        
    def refresh_data(self):
        '''
        Requests data about the orders the user has placed and saves it
        '''
        if not TESTING:
            #get products
            self.__catalog = get_refreshed_catalog(self.__page)

            #get orders
            header = {
                #"user_id": user_data["user_id"],
                #"manager_business_ids": user_data["manager_business_ids"]
            }

            url_template = Template(endpoints_urls["GET_ORDERS"])
            get_orders_url = url_template.safe_substitute(business_id=shared_vars["current_business"]["id"])

            try:
                response = requests.get(get_orders_url,headers =header)

                if response.status_code == STATUS_CODES["SUCCESS"]:
                    self.__orders = response["orders"]

                elif response.status_code >= STATUS_CODES["INTERNAL_ERROR"]:
                    present_snack_bar(self.__page, self.INTERNAL_ERROR_TEXT, "Red")
                else:
                    present_snack_bar(self.__page, self.UNRECOGNIZED_ERROR_TEXT, "Red")
                    
            except requests.exceptions.RequestException as e:
                present_snack_bar(self.__page, self.NETWORK_ERROR_TEXT, "Red")

    def __create_filter_button(self,state):
        button = Container(
            ElevatedButton(
                content = Text(
                    value=FILTER_BUTTON_TEXT[configs["LANGUAGE"]].get(state),
                    color = MAIN_TEXT_COLOR,
                    text_align=TextAlign.CENTER
                ),
                bgcolor= "transparent",
                color="#606060",
                adaptive = True,
                on_click = self.__change_filter_orders_list,
                data = state,
                width=120,
                style= ButtonStyle(
                    padding = padding.symmetric(10, 5),
                    overlay_color = BUTTON_OVERLAY_COLOR,
                    elevation = 0,
                    visual_density=VisualDensity.COMPACT
                ),
            ),
            width=120,
            gradient = Primary_Gradient(),
            border_radius=20,
            alignment=alignment.center
        )
        return button

    def __create_filters_row(self):
        '''
        Creates row with filter buttons
        ''' 
        self.__buttons_dict["waiting_validation"] = self.__create_filter_button("waiting_validation")
        
        self.__filters_row.controls.clear()
        self.__filters_row.controls.append(
            Column(
                controls=[
                    self.__waiting_validation_button,
                    self.__delivered_button
                ],
                alignment=MainAxisAlignment.END,
                spacing = 10
            ),
        )
        self.__filters_row.controls.append(
            Column(
                controls=[
                    self.__waiting_delivery_button,
                    self.__rejected_button,
                ],
                alignment=MainAxisAlignment.START,
                spacing = 10
            )
        )
        self.__filters_row.padding =padding.only(bottom = 100)

    def __fill_orders_column(self):
        '''
        Clears orders column and fills it with the orders according to __current_date and __current_filter
        '''
        #test order
        
        self.__orders=[{"order_id":"1","user_name":"aquele","order_date":"11/11/2010","order_data":[{"product_id":"01","quantity":2},{"product_id":"02","quantity":3}], "order_state":"waiting_delivery"},{"order_id":"3","user_name":"aquele","order_date":"11/11","order_data":[{"product_id":"04","quantity":2}],"order_state":"waiting_validation"}] #product_id as a name for test, change it later
        self.__catalog={"01":{"product_title":"Pao","product_price":2.0},"02":{"product_title":"Broa","product_price":2.5},"03":{"product_title":"Uma cena","product_price":4.0},"04":{"product_title":"Bolo","product_price":5.00}}
        if not self.__orders:
            return
         
        self.__orders_column.controls.clear()

        #get all orders given the day selected
        if self.__current_filter == "All":
            orders_to_show = self.__orders
        

        else:
            orders_to_show = [
                order for order in self.__orders
                if (order.get("order_state") == self.__current_filter)
            ]

        for order in orders_to_show:
            row =self.__create_new_order_row(order)
            self.__orders_column.controls.append(row)
        
    def __create_new_order_row(self, order: dict):
        '''
        Creates order row
        '''
        #print(order_string)
        return Container(
            Row(
                controls=[
                    Container(
                        content=Row(
                            controls=[
                                Container(
                                    content = Text(order["order_date"], color = MAIN_TEXT_COLOR),
                                    padding=padding.only(left=10, right=5),
                                    alignment= alignment.center_left
                                ),
                                Container(
                                    content=Text(FILTER_BUTTON_TEXT[configs["LANGUAGE"]].get(order.get("order_state")),color=MAIN_TEXT_COLOR),
                                    padding = padding.only(right=10),
                                    expand=True,
                                    alignment = alignment.center_right
                                )
                            ],
                            alignment=MainAxisAlignment.END
                            
                        ),
                        height=60,
                        expand=True,
                        gradient = Third_Gradient(),
                        border_radius=20,
                        alignment=alignment.center
                    ),
                    Container(
                        content = ElevatedButton(
                            opacity = 0.9,
                            content = Text("View", color = "MAIN_TEXT_COLOR"),
                            adaptive =True,
                            bgcolor="transparent",
                            color="#606060",
                            data = {"order_date":order["order_date"], "order_state":order["order_state"], "products":order["order_data"],"order_id":order["order_id"]},
                            on_click = self.__go_full_order_screen,
                            style = ButtonStyle(
                                elevation=0,
                                overlay_color="#fff791",
                                padding=Padding(left=2, top=1, right=2, bottom=1),
                                visual_density=VisualDensity.COMPACT
                            )
                        ),
                        width=60,
                        height=30,
                        gradient=Third_Gradient(),
                        border_radius=20,
                    ),
                ],
                alignment=MainAxisAlignment.START    
            ),
            padding=padding.only(left=10,right=10),
            expand=True
        )

    def __go_full_order_screen(self, e):
        
        products_dict={}

        for product in e.control.data["products"]:
            products_dict[self.__catalog[product["product_id"]]["product_title"]] = {
                "quantity": int(product["quantity"]),
                "quantity_text": product["quantity"],
                "cost" : self.__catalog[product["product_id"]]["product_price"]
                }

        shared_vars["current_order"] = {"products":products_dict, "date":e.control.data["order_date"], "state":e.control.data["order_state"],"order_id":e.control.data["order_id"]}
        shared_vars["main_container"].change_screen("full_order_screen")
    
    def __change_date_orders_list(self, e):
        '''
        Changes shown order according to the date chosen
        '''
        if e.control.data != self.__current_date:
            self.__current_date = e.control.data
            self.__fill_orders_column()
            self.__page.update()

    def __change_filter_orders_list(self, e):
        '''
        Change shown orders according to order status
        '''
        state = e.control.data

        if state != self.__current_filter:
            if self.__current_filter != "All":
                self.__buttons_dict[self.__current_filter].gradient = Primary_Gradient()
            self.__buttons_dict[state].gradient = Selected_Gradient()
            self.__current_filter = state
        else:
            if state != "All":
                self.__buttons_dict[state].gradient = Primary_Gradient()
            self.__current_filter = "All"
            
        self.__fill_orders_column()
        self.__page.update()
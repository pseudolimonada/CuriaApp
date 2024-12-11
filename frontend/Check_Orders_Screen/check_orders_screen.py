from flet import Column, MainAxisAlignment, Divider, ElevatedButton, Row, Page, ScrollMode, ButtonStyle, padding, Container, Text, CircleBorder, BorderSide, VisualDensity, TextStyle, Padding, alignment
from utils import get_refreshed_catalog, present_snack_bar, Selected_Gradient, Secondary_ElevatedButton_Container, Smart_TextField, Primary_Gradient, Secondary_Gradient, Third_Gradient
from shared import shared_vars, user_ids, endpoints_urls, STATUS_CODES,FILTER_BUTTON_TEXT, TESTING, MAIN_TEXT_COLOR
import requests
from string import Template

class Check_Orders_Screen(Column):
    '''
    Column that displays all the orders a user has made
    '''



    #Initializing useful variables
    __page = Page

    NETWORK_ERROR_TEXT: str = "Please verify your internet connection and try again..."

    __days_row: Row = Row(alignment = MainAxisAlignment.START, scroll = ScrollMode.ADAPTIVE)

    __filters_row: Row = Row(alignment = MainAxisAlignment.CENTER)

    __orders_column: Column = Column(alignment = MainAxisAlignment.START, scroll = ScrollMode.ADAPTIVE, expand = True)

    __current_date: str

    __current_filter = "All"

    __orders : list = []

    __catalog: dict
    

    #Constructor
    def __init__(self, page: Page):
        super().__init__(alignment = MainAxisAlignment.SPACE_BETWEEN, expand = True)

        self.__page = page
        
        self.refresh_data()

        self.__create_filters_row()
        self.__fill_orders_column()

        # Creating a column that joins order, filters and pages menu rows
        order_row_and_pages_menu_row = Column(
            controls=[
                Column(
                    controls=[
                        Divider(),
                        shared_vars["bottom_menu"]
                    ],
                    alignment=MainAxisAlignment.START,
                    spacing=4
                )
            ],
            alignment=MainAxisAlignment.START,
            spacing=40
        )

        # Updating controls of the screen
        self.controls = [
            Column(
                controls=[
                    Container(height=10),
                    self.__filters_row,
                    Divider(),
                    self.__orders_column,
                ],
                alignment=MainAxisAlignment.START,
                expand=True
            ),
            order_row_and_pages_menu_row,
            Divider()
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
                "user_id": user_ids["user_id"],
                "manager_business_ids": user_ids["manager_business_ids"]
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



    def __create_filters_row(self):
        '''
        Creates row with filter buttons
        ''' 

        #Appending a button in row for each filter in FILTER_BUTTON_TEXT
        self.__filters_row.controls.clear()
        for i in FILTER_BUTTON_TEXT.keys():
            self.__filters_row.controls.append(
                ElevatedButton(
                    text = FILTER_BUTTON_TEXT.get(i),
                    adaptive = True,
                    on_click = self.__change_filter_orders_list,
                    data = i,
                    style= ButtonStyle(
                        padding = padding.all(20),
                    ),
                )
            )


    
    def __fill_days_row(self):
        '''
        Clears the days row and refill it with new data from DB.
        '''        
        self.__days_row.controls.clear()
            
        self.__create_date_button("11/11")        
        self.__create_date_button("12/11")
        self.__create_date_button("13/11")
        self.__create_date_button("14/11")
        self.__create_date_button("15/11")

        self.__current_date = "11/11"


    def __fill_orders_column(self):
        '''
        Clears orders column and fills it with the orders according to __current_date and __current_filter
        '''
        #test order
        
        self.__orders=[{"order_id":"1","user_name":"aquele","order_date":"11/11","order_data":[{"product_id":"01","quantity":2},{"product_id":"02","quantity":3}], "order_state":"waiting_delivery"},{"order_id":"3","user_name":"aquele","order_date":"11/11","order_data":[{"product_id":"04","quantity":2}],"order_state":"waiting_validation"}] #product_id as a name for test, change it later
        self.__catalog={"01":{"product_title":"Pao","product_price":"2.0€"},"02":{"product_title":"Broa","product_price":"2.50€"},"03":{"product_title":"Uma cena","product_price":"4.0€"},"04":{"product_title":"Bolo","product_price":"5.00€"}}
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
        order_string = ""
        data = order.get("order_data")
        #print(data)
        '''
        for product in data:
            product_id = product.get("product_id")
            #print(product_id)
            order_string += self.__catalog[product_id]["product_title"] + " x" +str(product.get("quantity"))+", "
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
                                    padding=padding.only(left=10, right=20),
                                    alignment= alignment.center_left
                                ),
                                Container(
                                    content=Text(FILTER_BUTTON_TEXT.get(order.get("order_state")),color=MAIN_TEXT_COLOR),
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
        '''
        shared_vars["current_order"]
        {
        ["date] : "DD/MM/YYYY"
        ["state] : str
        ["products_title"] : [{"quantity":int, "product_id":, "cost": "1,50€", "quantity_text":},{},...]
        }
        '''
        #print(e.control.data["products"])
        
        products_dict={}

        for product in e.control.data["products"]:
            products_dict[self.__catalog[product["product_id"]]["product_title"]] = {
                "quantity": int(product["quantity"]),
                "quantity_text": product["quantity"],
                "cost" : self.__catalog[product["product_id"]]["product_price"]
                }

        shared_vars["current_order"] = {"products":products_dict, "date":e.control.data["order_date"], "state":e.control.data["order_state"],"order_id":e.control.data["order_id"]}
        user_ids["is_admin"] = True #remove later
        shared_vars["main_container"].change_screen("full_order_screen")



    def __create_date_button(self, date: str):
        '''
        Creates buttons for a date
        '''
        self.__days_row.controls.append(
            ElevatedButton(
                text = date,
                adaptive = True,
                on_click = self.__change_date_orders_list,
                data = date
            )
        )
    
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
        
        if e.control.data == self.__current_filter:
            self.__current_filter = "All"
            self.__fill_orders_column()
            self.__page.update()

        elif e.control.data != self.__current_filter:
            self.__current_filter = e.control.data
            self.__fill_orders_column()
            self.__page.update() 
        #print(self.__current_filter)
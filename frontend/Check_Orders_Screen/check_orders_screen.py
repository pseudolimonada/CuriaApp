from flet import Column, MainAxisAlignment, Divider, ElevatedButton, Row, Page, ScrollMode, ButtonStyle, padding, Container, Text, CircleBorder, BorderSide, VisualDensity

from shared import shared_vars, user_ids, endpoints_urls
import requests

class Check_Orders_Screen(Column):
    '''
    Column that displays all the orders a user has made
    '''



    #Button texts
    __page = Page
    __data = dict

    FILTER_BUTTON_TEXT: dict = {"waiting_validation":"Por aprovar", "waiting_delivery":"Por entregar", "delivered":"Entregue"} 

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
        header = {
            "user_id": user_ids["user_id"],
            "manager_business_ids": user_ids["manager_business_ids"]
        }
        #self.__catalog = requests.get(endpoints_urls["PRODUCTS"],headers=header)
        #self.__orders = requests.get(endpoints_urls["ORDERS"],headers=header)
    
    def __create_filters_row(self):
        '''
        Creates row with filter buttons
        ''' 
        self.__filters_row.controls.clear()
        for i in self.FILTER_BUTTON_TEXT.keys():
            self.__filters_row.controls.append(
                ElevatedButton(
                    text = self.FILTER_BUTTON_TEXT.get(i),
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
        # Add the new days buttons to controls according to data from DB


    def __fill_orders_column(self):
        '''
        Clears orders column and fills it with the orders according to __current_date and __current_filter
        '''
        #test order
        self.__orders=[{"order_id":"1","user_name":"aquele","order_date":"11/11","order_data":[{"product_id":"Croissant","quantity":2}], "order_state":"waiting_delivery"},{"order_id":"1","user_name":"aquele","order_date":"11/11","order_data":[{"product_id":"Pao","quantity":2}],"order_state":"waiting_validation"}] #product_id as a name for test, change it later
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
        print(data)
        for product in data:
            product_id = product.get("product_id")
            #print(product_id)
            order_string += product_id + " x" +str(product.get("quantity"))+", "
            

        #print(order_string)
        return Row(
            controls=[
                Container(
                    content=Row(
                        controls=[
                            Container(
                                content = Text(order_string),
                                padding=padding.only(left=10, right=20),
                                expand=True
                            )
                        ],
                        alignment = MainAxisAlignment.SPACE_AROUND
                    ),
                    height=80,
                    expand=True
                ),
                Container(
                    content=Text(self.FILTER_BUTTON_TEXT.get(order.get("order_state"))),
                )
            ]
        )


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
        print(self.__current_filter)
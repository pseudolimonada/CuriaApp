from flet import Column, MainAxisAlignment, Divider, ElevatedButton, Row, Page, ScrollMode, ButtonStyle, padding, Container, Text, CircleBorder, AlertDialog, TextButton, TextStyle, Padding, alignment
from shared import STATUS_CODES, user_ids, shared_vars, endpoints_urls
from present_snack_bar import present_snack_bar
from datetime import datetime, timedelta
from string import Template
import requests

class Order_Screen(Column):
    '''
    Column that represents a screen for the order realization
    '''
    
    ORDER_BUTTON_TEXT: str = "Order"
    ALERT_DIALOG_TITLE_TEXT: str = "Alert confirmation"
    ALERT_DIALOG_CONTENT_TEXT: str = "By changing the day your current order will be cleared. If you still want to continue, press 'OK', otherwise press CANCEL."
    ALERT_DIALOG_OK_TEXT: str = "OK"
    ALERT_DIALOG_CANCEL_TEXT: str = "CANCEL"
    
    __page: Page
    __catalog: dict = {}
    __current_week_catalog: dict = {}
    
    __current_order: dict = {
        "date": datetime,
        "products": dict
    }
    __total_amount: int = 0
    __current_date: datetime
    __current_week_day: str
    
    __days_row: Row = Row(
        alignment=MainAxisAlignment.CENTER,
        run_spacing=5,
        wrap=True
        #scroll=ScrollMode.ADAPTIVE
    )
    
    __products_column: Column = Column(
        alignment=MainAxisAlignment.START,
        scroll=ScrollMode.ADAPTIVE,
        expand=True
    )
    
    __order_row: Row = Row(
        alignment=MainAxisAlignment.CENTER
    )
    
    __order_button: ElevatedButton
    
    __alert = AlertDialog(
        modal=True,
        title=Text(ALERT_DIALOG_TITLE_TEXT),
        content=Text(ALERT_DIALOG_CONTENT_TEXT),
        actions_alignment=MainAxisAlignment.END
    )
    
    # Constructor
    def __init__(
        self,
        page: Page
    ):
        super().__init__(alignment=MainAxisAlignment.SPACE_BETWEEN, expand=True)
        
        self.__page = page
        
        # Get today's date
        self.__current_date = datetime.today()
        self.__current_week_day = self.__current_date.strftime("%A")
        
        self.refresh_data()
        
        # Setting up order button (starts disabled)
        self.__order_button = ElevatedButton(
            text=self.ORDER_BUTTON_TEXT,
            adaptive=True,
            disabled=True,
            on_click=self.__realize_order,
            style=ButtonStyle(
                padding=padding.symmetric(10, 70)
            ),
            scale=1.6
        )
        
        # Updating the controls of the order row with the button
        self.__order_row.controls = [self.__order_button]
        
        # Creating a column that joins order and pages menu rows
        order_row_and_pages_menu_row = Column(
            controls=[
                Divider(),
                self.__order_row,
                Column(
                    controls=[
                        Divider(),
                        shared_vars["bottom_menu"],
                        Divider()
                    ],
                    alignment=MainAxisAlignment.START,
                    spacing=1
                )
            ],
            alignment=MainAxisAlignment.START,
            spacing=20
        )
        
        # Updating controls of the screen
        self.controls = [
            Column(
                controls=[
                    Divider(),
                    Container(
                        content = self.__days_row,
                        padding=Padding(left=8, top=2, right=8, bottom=2),
                        alignment=alignment.center
                    ),
                    Divider(),
                    self.__products_column,
                ],
                alignment=MainAxisAlignment.START,
                expand=True
            ),
            order_row_and_pages_menu_row
        ]
    
    # Refresh data about the days and products by full filling the rows and columns info again
    def refresh_data(self):
        '''
        Refresh data about the days and products by full filling the rows and columns info again.
        '''
        
        # Calculate the number of days to subtract to get to Monday
        days_to_monday = self.__current_date.weekday()  # weekday() returns 0 for Monday, 1 for Tuesday, etc.
        # Subtract the number of days to get to Monday
        monday = self.__current_date - timedelta(days=days_to_monday)
        
        ###########################################################################
        #        ------- REMOVE THIS IF CASE FOR REAL TEST !!!!!!! -------        #
        ###########################################################################
        testing = True
        if testing:
            self.__current_order["products"] = {}
            for i in range(20):
                self.__current_order["products"][f"Este é um Pao disto assim {i}"] = {
                    "quantity_text": Text(value="0"),
                    "quantity": 0,
                    "cost": "1.50€"
                }
            self.__current_order["date"] = self.__current_date
            self.__fill_days_row(monday)
            self.__fill_products_column()
            return
        
        if self.__refresh_catalog(self):
            if self.__refresh_week_catalog(self, str(monday)):
                # Initialize all the available products
                self.__current_order["products"] = {}
                for product_id in self.__catalog.keys():
                    self.__current_order["products"][self.__catalog[product_id]["product_title"]] = {
                        "quantity_text": Text(value="0"),
                        "quantity": 0,
                        "cost": self.__catalog[product_id]["product_price"]
                    }
                
                self.__current_order["date"] = self.__current_date
                self.__fill_days_row(monday)
                self.__fill_products_column()
    
    # Refreshes the catalog for the actual business and save it in self.__catalog
    # If any error occurs return false, otherwise return true
    # Catalog Structure:
    #   {
    #       "product_id1": {
    #           "image_url":"(opt)",
    #           "product_title":"...",
    #           "product_description":"...",
    #           "product_price":"...",
    #           "product_scarcity": (5 or 1 or null)
    #       },
    #       "product_id2": {
    #           ...
    #       },
    #   }
    #
    def __refresh_catalog(self):
        headers = {
            "user_id": user_ids["user_id"],
            "manager_business_ids": user_ids["manager_business_ids"]
        }
        url_template = Template(endpoints_urls["GET_CATALOG"])
        get_catalog_url = url_template.safe_substitute(business_id=user_ids["manager_business_ids"][0])
        
        try:
            # Sending request and getting response
            response = requests.get(get_catalog_url, headers=headers)
            
            # Check the response
            if response.status_code == STATUS_CODES["SUCCESS"]:
                # Save the refreshed catalog
                self.__catalog = response["catalog"]
                return True
            elif response.status_code >= STATUS_CODES["INTERNAL_ERROR"]:
                present_snack_bar(self.__page, self.INTERNAL_ERROR_TEXT, "Red")
            else:
                present_snack_bar(self.__page, self.UNRECOGNIZED_ERROR_TEXT, "Red")
        except requests.exceptions.RequestException as e:
            # Handle network-related errors
            present_snack_bar(self.__page, self.NETWORK_ERROR_TEXT, "Red")
        
        return False
        
    # Refreshes the week catalog for the actual business and save it in self.__current_week_catalog
    # If any error occurs return false, otherwise return true
    # Week Catalog Structure:
    #   {
    #       "Mon": ["product_id", "product_id", "product_id", "..."],
    #       "Tue": ["product_id", "product_id", "product_id", "..."],
    #       "Wed": ["product_id", "product_id", "product_id", "..."],
    #       "Thu": ["product_id", "product_id", "product_id", "..."],
    #       "Fri": ["product_id", "product_id", "product_id", "..."],
    #       "Sat": ["product_id", "product_id", "product_id", "..."],
    #       "Sun": ["product_id", "product_id", "product_id", "..."]
    #   }
    #
    def __refresh_week_catalog(
        self,
        monday_date:str
    ):
        headers = {
            "user_id": user_ids["user_id"],
            "manager_business_ids": user_ids["manager_business_ids"]
        }
        params = {
            "monday_date": monday_date,
        }
        url_template = Template(endpoints_urls["GET_CATALOG"])
        get_catalog_url = url_template.safe_substitute(business_id=user_ids["manager_business_ids"][0])
        
        try:
            # Sending request and getting response
            response = requests.get(get_catalog_url, headers=headers, params=params)
            
            # Check the response
            if response.status_code == STATUS_CODES["SUCCESS"]:
                # Saving the catalog for each day
                self.__current_week_catalog["Mon"] = response["Mon"]
                self.__current_week_catalog["Tue"] = response["Tue"]
                self.__current_week_catalog["Wed"] = response["Wed"]
                self.__current_week_catalog["Thu"] = response["Thu"]
                self.__current_week_catalog["Fri"] = response["Fri"]
                self.__current_week_catalog["Sat"] = response["Sat"]
                self.__current_week_catalog["Sun"] = response["Sun"]
                return True
                
            elif response.status_code >= STATUS_CODES["INTERNAL_ERROR"]:
                present_snack_bar(self.__page, self.INTERNAL_ERROR_TEXT, "Red")
            else:
                present_snack_bar(self.__page, self.UNRECOGNIZED_ERROR_TEXT, "Red")
        except requests.exceptions.RequestException as e:
            # Handle network-related errors
            present_snack_bar(self.__page, self.NETWORK_ERROR_TEXT, "Red")
        
        return False
    
    # Clears the days row and refill it with new data
    def __fill_days_row(
        self,
        monday: datetime
    ):
        '''
        Clears the days row and refill it with new data from DB.
        '''
        
        self.__days_row.controls.clear()
        
        self.__create_new_date_button("Mon", monday)
        self.__create_new_date_button("Tue", (monday + timedelta(days=1)))
        self.__create_new_date_button("Wed", (monday + timedelta(days=2)))
        self.__create_new_date_button("Thu", (monday + timedelta(days=3)))
        self.__create_new_date_button("Fri", (monday + timedelta(days=4)))
        self.__create_new_date_button("Sat", (monday + timedelta(days=5)))
        self.__create_new_date_button("Sun", (monday + timedelta(days=6)))
        
    # Clears the products column and refill it with new data from DB for a specific date
    def __fill_products_column(self):
        '''
        Clears the products column and refill it with new data from DB for a specific date.
        '''
        
        self.__products_column.controls.clear()
        
        ###########################################################################
        #        ------- REMOVE THIS IF CASE FOR REAL TEST !!!!!!! -------        #
        ###########################################################################
        testing = True
        if testing:
            if self.__current_week_day == "Wed":
                num = 20
            elif self.__current_week_day == "Thu":
                num = 5
            elif self.__current_week_day == "Fri":
                num = 2
            else:
                num = 0
            for i in range(num):
                    product_row = self.__create_new_product_row(f"Este é um Pao disto assim {i}", self.__current_order["products"][f"Este é um Pao disto assim {i}"]["cost"])
                    self.__products_column.controls.append(product_row)
            return
        
        # Add products rows according to the products in the catalog day
        for id_product in self.__current_week_catalog[self.__current_week_day]:
                product_row = self.__create_new_product_row(self.__catalog[id_product]["product_title"], self.__catalog[id_product]["product_price"])
                self.__products_column.controls.append(product_row)
    
    # Realizes an order when clicked in order_button
    def __realize_order(self, e):
        shared_vars["current_order"] = self.__current_order
        shared_vars["main_container"].change_screen("full_order_screen")
    
    # Creates and returns a button for a respective date
    def __create_new_date_button(
        self,
        week_day: str,
        date: datetime
    ):
        '''
        Creates and appends to the days list a button for a respective date.
        '''
        
        self.__days_row.controls.append(
            ElevatedButton(
                text=week_day,
                adaptive=True,
                on_click=self.__change_date_product_list,
                data=(week_day, date),
                width=60,
                height=30,
                style=ButtonStyle(
                    padding=Padding(left=2, top=1, right=2, bottom=1),
                    text_style=TextStyle(size=14)
                )
            )
        )
        
    # Changes the products list according to the date selected
    def __change_date_product_list(self, e):
        '''
        Changes the products list according to the date selected.
        '''
        
        if e.control.data[1] != self.__current_date:
            if self.__total_amount > 0:
                self.__alert.actions=[
                    TextButton(self.ALERT_DIALOG_OK_TEXT, on_click=self.__handle_close_dialog, data=e.control.data),
                    TextButton(self.ALERT_DIALOG_CANCEL_TEXT, on_click=self.__handle_close_dialog)
                ]
                self.__page.open(self.__alert)
            else:
                self.__current_date = e.control.data[1]
                self.__current_week_day = e.control.data[0]
                self.__current_order["date"] = self.__current_date
                self.__fill_products_column()
                self.__page.update()
    
    # Handles the close of the dialog alert
    def __handle_close_dialog(self, e):
        '''
        Handles the close of the dialog alert.
        '''
        
        self.page.close(self.__alert)
        if e.control.text == self.ALERT_DIALOG_OK_TEXT:
            for product in self.__current_order["products"]:
                self.__current_order["products"][product]["quantity"] = 0
                self.__current_order["products"][product]["quantity_text"].value = "0"
            self.__current_date = e.control.data[1]
            self.__current_week_day = e.control.data[0]
            self.__current_order["date"] = self.__current_date
            self.__order_button.disabled = True
            self.__total_amount = 0
            self.__fill_products_column()
            
        self.__page.update()
    
    # Creates and returns a row with the information about the product and two buttons ('+' and '-')
    def __create_new_product_row(
        self,
        product_name: str,
        product_cost: str
    ):
        '''
        Creates and returns a row with the information about the product and two buttons ('+' and '-').
        '''
        
        return Row(
            controls=[
                Container(
                    content=Row(
                        controls=[
                            Container(
                                content=Text(product_name),
                                padding=padding.only(left=10, right=20),
                                expand=True
                            ),
                            Text(product_cost),
                        ],
                        alignment=MainAxisAlignment.SPACE_AROUND
                    ),
                    height=80,
                    expand=True
                ),
                Container(
                    content=Row(
                        controls=[
                            Container(
                                content=ElevatedButton(
                                    text="-",
                                    adaptive=True,
                                    style=ButtonStyle(
                                        shape=CircleBorder(),
                                        padding=padding.all(0)
                                    ),
                                    on_click=self.__change_product_amount,
                                    data=("-", product_name)
                                ),
                                width=40,
                                height=40
                            ),
                            self.__current_order["products"][product_name]["quantity_text"],
                            Container(
                                content=ElevatedButton(
                                    text="+",
                                    adaptive=True,
                                    style=ButtonStyle(
                                        shape=CircleBorder(),
                                        padding=padding.all(0)
                                    ),
                                    on_click=self.__change_product_amount,
                                    data=("+", product_name)
                                ),
                                padding=padding.only(right=10),
                                width=50,
                                height=40
                            )
                        ],
                        alignment=MainAxisAlignment.START,
                        spacing=10,
                        expand=True
                    )
                )
            ]
        )
        
    # Changes the product amount in the current order list.
    def __change_product_amount(self, e):
        '''
        Changes the product amount in the current order list.
        '''
        
        if e.control.data[0] == "+":
            self.__current_order["products"][e.control.data[1]]["quantity"] += 1
            self.__total_amount += 1
            if self.__total_amount > 0:
                self.__order_button.disabled = False
        elif e.control.data[0] == "-":
            if self.__current_order["products"][e.control.data[1]]["quantity"] > 0:
                self.__current_order["products"][e.control.data[1]]["quantity"] -= 1
                self.__total_amount -= 1
                if self.__total_amount <= 0:
                    self.__order_button.disabled = True
                    
        self.__current_order["products"][e.control.data[1]]["quantity_text"].value = f"{self.__current_order["products"][e.control.data[1]]["quantity"]}"
        
        self.__page.update()
    
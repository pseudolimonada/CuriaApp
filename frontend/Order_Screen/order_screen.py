from flet import Column, MainAxisAlignment, Divider, ElevatedButton, Row, Page, ScrollMode, ButtonStyle, padding, Container, Text, CircleBorder, AlertDialog, TextButton
from shared import shared_vars
import requests

class Order_Screen(Column):
    '''
    
    '''
    
    
    ORDER_BUTTON_TEXT: str = "Order"
    ALERT_DIALOG_TITLE_TEXT: str = "Alert confirmation"
    ALERT_DIALOG_CONTENT_TEXT: str = "By changing the day your current order will be cleared. If you still want to continue, press 'OK', otherwise press CANCEL."
    ALERT_DIALOG_OK_TEXT: str = "OK"
    ALERT_DIALOG_CANCEL_TEXT: str = "CANCEL"
    
    __page: Page
    __data: dict
    
    __current_order: dict = {
        "date": str,
        "products": dict
    }
    __total_amount: int = 0
    __current_date: str
    
    __days_row: Row = Row(
        alignment=MainAxisAlignment.START,
        scroll=ScrollMode.ADAPTIVE
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
                    self.__days_row,
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
        
        self.__current_order["products"] = {}
        
        # Send request to DB and receive data about the products and days and fill the __data variable with them
        for i in range(20):
            self.__current_order["products"][f"Este é um Pao disto Daquilo e do Outro {i}"] = {
                "quantity_text": Text(value="0"),
                "quantity": 0,
                "cost": 1.5
            }
            
        self.__fill_days_row()
        self.__fill_products_column()
        
    # Clears the days row and refill it with new data from DB
    def __fill_days_row(self):
        '''
        Clears the days row and refill it with new data from DB.
        '''
        
        self.__days_row.controls.clear()
        
        self.__create_new_date_button("11/11")
        self.__create_new_date_button("12/11")
        self.__create_new_date_button("13/11")
        self.__create_new_date_button("14/11")
        self.__create_new_date_button("15/11")
        self.__current_date = "15/11"
        self.__current_order["date"] = self.__current_date
        # Add the new days buttons to controls according to data from DB
        
    # Clears the products column and refill it with new data from DB for a specific date
    def __fill_products_column(self):
        '''
        Clears the products column and refill it with new data from DB for a specific date.
        '''
        
        self.__products_column.controls.clear()
        
        if self.__current_date == "15/11":
            for i in range(2):
                product = self.__create_new_product_row(f"Este é um Pao disto Daquilo e do Outro {i}", self.__current_order["products"][f"Este é um Pao disto Daquilo e do Outro {i}"]["cost"])
                self.__products_column.controls.append(product)
        elif self.__current_date == "14/11":
            for i in range(20):
                product = self.__create_new_product_row(f"Este é um Pao disto Daquilo e do Outro {i}", self.__current_order["products"][f"Este é um Pao disto Daquilo e do Outro {i}"]["cost"])
                self.__products_column.controls.append(product)
        # Add the new products info and buttons to controls according to data from DB
    
    # Realizes an order when clicked in order_button
    def __realize_order(self, e):
        shared_vars["current_order"] = self.__current_order
        shared_vars["main_container"].change_screen("full_order_screen")
    
    # Creates and returns a button for a respective date
    def __create_new_date_button(
        self,
        date: str
    ):
        '''
        Creates and appends to the days list a button for a respective date.
        '''
        
        self.__days_row.controls.append(
            ElevatedButton(
                text=date,
                adaptive=True,
                on_click=self.__change_date_product_list,
                data=date
            )
        )
        
    # Changes the products list according to the date selected
    def __change_date_product_list(self, e):
        '''
        Changes the products list according to the date selected.
        '''
        
        if e.control.data != self.__current_date:
            if self.__total_amount > 0:
                self.__alert.actions=[
                    TextButton(self.ALERT_DIALOG_OK_TEXT, on_click=self.__handle_close_dialog, data=e.control.data),
                    TextButton(self.ALERT_DIALOG_CANCEL_TEXT, on_click=self.__handle_close_dialog)
                ]
                self.__page.open(self.__alert)
            else:
                self.__current_date = e.control.data
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
            self.__current_date = e.control.data
            self.__current_order["date"] = self.__current_date
            self.__order_button.disabled = True
            self.__total_amount = 0
            self.__fill_products_column()
            
        self.__page.update()
    
    # Creates and returns a row with the information about the product and two buttons ('+' and '-')
    def __create_new_product_row(
        self,
        product_name: str,
        product_cost: float
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
                            Text(f"{product_cost:.2f}€"),
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
    
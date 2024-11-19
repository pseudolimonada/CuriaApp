from flet import Column, MainAxisAlignment, Divider, ElevatedButton, Row, Page, ScrollMode, ButtonStyle, padding, Container, Text, CircleBorder, BorderSide
from shared import shared_vars
import requests

class Order_Screen(Column):
    '''
    
    '''
    
    
    ORDER_BUTTON_TEXT: str = "Order"
    
    __page: Page
    __data: dict
    
    __current_order: dict = {}
    __total_amount: int = 0
    
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
        
        # Send request to DB and receive data about the products and days and fill the __data variable with them
        for i in range(10):
            self.__current_order[f"product {i}"] = 0
        
        self.__fill_days_row()
        self.__fill_products_column("15/11")
        
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
        # Add the new days buttons to controls according to data from DB
        
    # Clears the products column and refill it with new data from DB for a specific date
    def __fill_products_column(self, date):
        '''
        Clears the products column and refill it with new data from DB for a specific date.
        '''
        
        self.__products_column.controls.clear()
        
        if date == "15/11":
            for i in range(2):
                product = self.__create_new_product_row(f"product {i}", "1,50€")
                self.__products_column.controls.append(product)
        elif date == "14/11":
            for i in range(10):
                product = self.__create_new_product_row(f"product {i}", "1,50€")
                self.__products_column.controls.append(product)
        # Add the new products info and buttons to controls according to data from DB
    
    # Realizes an order when clicked in order_button
    def __realize_order(self, e):
        print("Test")
        pass
    
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
        
        self.__fill_products_column(e.control.data)
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
                                Text(product_name),
                                Text(product_cost),
                            ],
                            alignment=MainAxisAlignment.SPACE_AROUND,
                    ),
                    width=200,
                    height=30
                ),
                Container(
                    content=Row(
                        controls=[
                            ElevatedButton(
                                text="+",
                                adaptive=True,
                                style=ButtonStyle(
                                    shape=CircleBorder(),
                                    padding=padding.all(0)
                                ),
                                on_click=self.__change_product_amount,
                                data=("+", product_name)
                            ),
                            ElevatedButton(
                                text="-",
                                adaptive=True,
                                style=ButtonStyle(
                                    shape=CircleBorder(),
                                    padding=padding.all(0)
                                ),
                                on_click=self.__change_product_amount,
                                data=("-", product_name)
                            )
                        ],
                        alignment=MainAxisAlignment.START,
                        spacing=1,
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
            self.__current_order[e.control.data[1]] += 1
            self.__total_amount += 1
            if self.__total_amount > 0:
                self.__order_button.disabled = False
        elif e.control.data[0] == "-":
            if self.__current_order[e.control.data[1]] > 0:
                self.__current_order[e.control.data[1]] -= 1
                self.__total_amount -= 1
                if self.__total_amount <= 0:
                    self.__order_button.disabled = True
        
        self.__page.update()
    
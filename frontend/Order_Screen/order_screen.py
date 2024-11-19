from flet import Column, MainAxisAlignment, Divider, ElevatedButton, Row, Page, ScrollMode, ButtonStyle, padding
from shared import shared_vars

class Order_Screen(Column):
    '''
    
    '''
    
    ORDER_BUTTON_TEXT: str = "Order"
    
    __data: dict
    
    __days_row: Row = Row(
        alignment=MainAxisAlignment.START,
        scroll=ScrollMode.HIDDEN
    )
    __products_column: Column = Column(
        alignment=MainAxisAlignment.START,
        scroll=ScrollMode.HIDDEN
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
                self.__order_row,
                Column(
                    controls=[
                        Divider(),
                        shared_vars["bottom_menu"]
                    ],
                    alignment=MainAxisAlignment.START,
                    spacing=5
                )
            ],
            alignment=MainAxisAlignment.START,
            spacing=40
        )
        
        # Updating controls of the screen
        self.controls = [
            self.__days_row,
            self.__products_column,
            order_row_and_pages_menu_row
        ]
    
    # Refresh data about the days and products by full filling the rows and columns info again
    def refresh_data(self):
        '''
        Refresh data about the days and products by full filling the rows and columns info again.
        '''
        
        # Send request to DB and receive data about the products and days and fill the __data variable with them
        
        self.__fill_days_row()
        self.__fill_products_column()
        
    # Clears the days row and refill it with new data from DB
    def __fill_days_row(self):
        '''
        Clears the days row and refill it with new data from DB.
        '''
        
        self.__days_row.controls.clear()
        
        # Add the new days buttons to controls according to data from DB
        
    # Clears the products column and refill it with new data from DB
    def __fill_products_column(self):
        '''
        Clears the products column and refill it with new data from DB.
        '''
        
        self.__products_column.controls.clear()
        
        # Add the new products info and buttons to controls according to data from DB
    
    # Realizes an order when clicked in order_button
    def __realize_order(self, e):
        print("Test")
        pass
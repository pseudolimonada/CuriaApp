from flet import Column, padding, CrossAxisAlignment, MainAxisAlignment, Page, ElevatedButton, ScrollMode, Text, icons, Divider, Row, Container
from shared import shared_vars

class Full_Order_Screen(Column):
    '''
    
    '''

    TITLE_TEXT: str = "Order to day: "
    SUB_TITLE: str = "Order State: "
    CONFIRM_BUTTON_TEXT: str = "Confirm!"
    CANCEL_BUTTON_TEXT: str = "Cancel"
    BACK_BUTTON_TEXT: str = "Back"

    __page: Page
    
    __title_column: Column = Column(
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER
    )
    
    __products_column: Column = Column(
        alignment=MainAxisAlignment.START,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        scroll=ScrollMode.ADAPTIVE,
        expand=True
    )
    
    __buttons_row: Row = Row(
        alignment=MainAxisAlignment.CENTER,
        vertical_alignment=CrossAxisAlignment.CENTER
    )
    
    __confirm_order_button: ElevatedButton
    __cancel_button: ElevatedButton
    __back_button: ElevatedButton

    def __init__(
        self,
        page: Page
    ):
        super().__init__(
            controls=[
                self.__title_column,
                self.__products_column,
                Column(
                    controls=[
                        Divider(),
                        self.__buttons_row,
                        Divider(),
                    ],
                    alignment=MainAxisAlignment.CENTER
                ),
            ],
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            expand=True
        )
        
        self.__page = page
        
        self.__confirm_order_button = ElevatedButton(
            text=self.CONFIRM_BUTTON_TEXT,
            icon=icons.CHECK,
            adaptive=True,
            on_click=self.__confirm_order,
        )
        
        self.__cancel_button = ElevatedButton(
            text=self.CANCEL_BUTTON_TEXT,
            icon=icons.CANCEL,
            adaptive=True,
            on_click=self.__cancel_order,
        )
        
        self.__back_button = ElevatedButton(
            text=self.CANCEL_BUTTON_TEXT,
            icon=icons.KEYBOARD_RETURN,
            adaptive=True,
            on_click=self.__turn_back,
            scale=1.5
        )
        
    def set_confirm_order_layout(self):
        # Resetting controls from before
        self.__products_column.controls.clear()
        self.__buttons_row.controls.clear()
        
        # Setting the
        self.__title_column.controls=[
            Divider(),
            Text(value=f"{self.TITLE_TEXT}{shared_vars["current_order"]["date"]}"),
            Divider()
        ]
        
        products_dict: dict = shared_vars["current_order"]["products"]
        for product in products_dict:
            if products_dict[product]["quantity"] > 0:
                self.__products_column.controls.append(self.__create_new_product_row(product, products_dict[product]["quantity"], products_dict[product]["cost"]))
        
        self.__buttons_row.controls.append(self.__cancel_button)
        self.__buttons_row.controls.append(self.__confirm_order_button)
        
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
        
        return Row(
            controls=[
                Text(value=f"{product_name} x{product_quantity}"),
                Text(f"{product_quantity*product_cost}€"),
            ],
            alignment=MainAxisAlignment.SPACE_AROUND,
        )
        
    
    def __confirm_order(self, e):
        print("Test")
        pass
    
    def __cancel_order(self, e):
        shared_vars["main_container"].change_screen("order_screen")
        
    def set_order_details_layout(self):
        pass
    
    def __turn_back(self, e):
        pass
from flet import Row, MainAxisAlignment, IconButton, icons
from shared import shared_vars

class Bottom_Menu(Row):
    '''
    Row that have 2 icon buttons that represents the bottom menu.
    '''

    __order_page_button: IconButton
    __check_orders_page_button: IconButton

    # Constructor
    def __init__(self):
        super().__init__(alignment=MainAxisAlignment.SPACE_EVENLY)

        self.__order_page_button = IconButton(
            adaptive=True,
            enable_feedback=False,
            icon_size=30,
            on_click= self.__go_to_order_screen,
            icon=icons.BORDER_COLOR
        )
        
        self.__check_orders_page_button = IconButton(
            adaptive=True,
            enable_feedback=False,
            icon_size=30,
            on_click= self.__go_to_check_orders_screen,
            icon=icons.FORMAT_LIST_BULLETED
        )

        self.controls = [
            self.__order_page_button,
            self.__check_orders_page_button
        ]
        
    # Changes to order screen if it is not already
    def __go_to_order_screen(self, e):
        '''
        Changes to order screen if it is not already.
        '''
        
        if shared_vars["main_container"].selected_screen_name != "order_screen":
            shared_vars["main_container"].change_screen("order_screen")
        else:
            pass
    
    # Changes to check orders screen if it is not already
    def __go_to_check_orders_screen(self, e):
            '''
            Changes to check orders screen if it is not already.
            '''
            
            if shared_vars["main_container"].selected_screen_name != "check_orders_screen":
                shared_vars["main_container"].change_screen("check_orders_screen")
            else:
                pass
from flet import (
    Container, Page, Theme, ColorScheme, colors, alignment, 
    LinearGradient, BorderRadius, Offset, BoxShadow
                  )
from utils import present_snack_bar
from shared import THIRD_GRADIENT_COLOR_1, MAIN_TEXT_COLOR, BG_TOP_COLOR, BG_BOTTOM_COLOR, user_ids, shared_vars

class Main_Container(Container):
    '''
    Main Container where everything will be placed and displayed.
    Represent the screen itself.
    '''
    
    __page: Page
    __screens_dict: dict = {}
    selected_screen_name: str = ""
    CHANGE_SCREEN_ERROR_TEXT: str = "Screen doesn't exist..."
    CURRENT_SCREEN_NOT_RECOGNIZED: str = "Screen can't load because of an internal error..."
    
    # Constructor 
    def __init__(
        self,
        page: Page
    ):
        super().__init__(
            expand=True,
            gradient=LinearGradient(
                begin=alignment.top_center,
                end=alignment.bottom_center,
                colors=[
                    BG_TOP_COLOR,
                    BG_BOTTOM_COLOR
                ],
            ),
            alignment=alignment.center
        )
        self.__page = page
    
    # Adds the screen to the screens list and attributes a name to the screen.
    def add_screen_to_list(
        self,
        screen,
        screen_name: str
    ):
        '''
        Adds the screen to the screens dict and attributes a name to the screen (the key of the dict).

        screen: Object that represents a screen.
        screen_name: String that will be added as the name of the screen.
        '''
        
        self.__screens_dict[screen_name] = screen
    
    # Changes the current screen for another screen by giving the screen name.
    def change_screen(
        self,
        screen_name: str
    ):
        '''
        Changes the current screen for another screen by giving the screen name.
        
        screen_name: String that represents the screen.
        '''
        
        if screen_name in self.__screens_dict.keys():
            if screen_name == "full_order_screen":
                if self.selected_screen_name == "order_screen":
                    self.__screens_dict[screen_name].set_confirm_order_layout()
                elif self.selected_screen_name == "check_orders_screen":
                    self.__screens_dict[screen_name].set_order_details_layout()
                else:
                    present_snack_bar(self.__page, self.CURRENT_SCREEN_NOT_RECOGNIZED, "Red")
                    return
            elif screen_name == "order_screen":
                if not user_ids["is_admin"] and self.selected_screen_name == "full_order_screen":
                    self.__screens_dict[screen_name].reset_current_order()
                    self.__screens_dict[screen_name].refresh_data(False)
                
                shared_vars["bottom_menu"].controls[0].icon_color = THIRD_GRADIENT_COLOR_1
                shared_vars["bottom_menu"].controls[1].icon_color = MAIN_TEXT_COLOR
            elif screen_name == "check_orders_screen":
                shared_vars["bottom_menu"].controls[0].icon_color = MAIN_TEXT_COLOR
                shared_vars["bottom_menu"].controls[1].icon_color = THIRD_GRADIENT_COLOR_1
            
            self.selected_screen_name = screen_name
            self.content = self.__screens_dict[screen_name]
            self.__page.update()
        else:
            present_snack_bar(self.__page, self.CHANGE_SCREEN_ERROR_TEXT, "Red")
        
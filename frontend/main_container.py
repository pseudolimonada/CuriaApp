from flet import Container, Column, Page
from present_snack_bar import present_snack_bar

class Main_Container(Container):
    '''
    Main Container where everything will be placed and displayed.
    Represent the screen itself.
    '''
    
    __page: Page
    __screens_dict: dict = {}
    selected_screen_name: str = ""
    CHANGE_SCREEN_ERROR_TEXT: str = "Screen doesn't exist..."
    
    # Constructor 
    def __init__(
        self,
        page: Page
    ):
        super().__init__(expand=True)
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
            self.selected_screen_name = screen_name
            self.content = self.__screens_dict[screen_name]
        else:
            present_snack_bar(self.__page, self.CHANGE_SCREEN_ERROR_TEXT, "Red")
        
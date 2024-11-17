from flet import Container

class Main_Container(Container):
    '''
    Main Container where everything will be placed and displayed.
    Represent the screen itself.
    '''
        
    selected_screen_name: str = ""
        
    def __init__(self):
        super().__init__(expand=True)
            
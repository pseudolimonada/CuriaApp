from flet import Column, MainAxisAlignment, ElevatedButton, TextField, Row, Page

class Order_Screen(Column):
    '''
    
    '''
    
    # Constructor
    def __init__(
        self,
        page: Page
    ):
        super().__init__(alignment=MainAxisAlignment.SPACE_EVENLY, expand=True)
        
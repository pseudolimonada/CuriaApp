from flet import Column, MainAxisAlignment, ElevatedButton, TextField, Row, Page

class Login_Screen(Column):
    '''
    Column that represents a screen for Login / Register of the user
    '''
    
    # TextFields
    name_textfield: TextField = TextField(label="User Name", hint_text="Insert Your User Name Here", max_length=40)
    password_textfield: TextField = TextField(label="Password", hint_text="Insert Your Password Here", max_length=40)
    credentials_column: Column
    
    # Buttons
    login_button: ElevatedButton = ElevatedButton(text="LOGIN", scale=1.5)
    register_button: ElevatedButton = ElevatedButton(text="REGISTER", scale=1)
    login_register_column: Column
    
    # Constructor
    def __init__(
        self,
        page: Page
    ):
        super().__init__(alignment=MainAxisAlignment.SPACE_EVENLY, expand=True)
        
        # Setting the column with the text fields
        self.credentials_column = Column(
            controls=[
                Row(controls=[self.name_textfield], alignment=MainAxisAlignment.CENTER),
                Row(controls=[self.password_textfield], alignment=MainAxisAlignment.CENTER)
            ],
            alignment=MainAxisAlignment.CENTER
        )
        
        # Setting the column with the buttons
        self.login_button.on_click = Login_Screen.login
        self.register_button.on_click = Login_Screen.register
        self.login_register_column = Column(
            controls=[
                Row(controls=[self.login_button], alignment=MainAxisAlignment.CENTER),
                Row(controls=[self.register_button], alignment=MainAxisAlignment.CENTER),
            ],
            alignment=MainAxisAlignment.CENTER,
            spacing=20
        )
        
        # Setting the controls of the screen (column) with all elements
        self.controls = [
            self.credentials_column,
            self.login_register_column
        ]

    def login(e):
        '''
        Verifies in DB if the inserted credentials exist and are valid. If they are makes the transition to the orders screen.
        '''
        pass

    def register(e):
        pass